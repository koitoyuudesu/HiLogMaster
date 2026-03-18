import os
import re
import patoolib
import chardet
from typing import Optional, List
import tempfile
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogParser:
    """Core log parsing functionality for LogMaster AI."""
    
    LOG_PATTERN = re.compile(r"\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}.* E .*")
    
    def __init__(self, keyword: str, context_lines: int = 1):
        self.keyword = keyword
        self.context_lines = context_lines
    
    def process_input(self, input_path: str) -> Optional[str]:
        """Main entry point - processes either a zip, rar or txt file."""
        try:
            if input_path.endswith('.txt'):
                return self._process_single_file(input_path)
            else:
                return self._process_archive(input_path)
        except Exception as e:
            logger.error(f"Error processing {input_path}: {e}")
            return None
    
    def _process_archive(self, archive_path: str) -> Optional[str]:
        """Process zip/rar archive to find and parse log files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Extract archive
                patoolib.extract_archive(archive_path, outdir=temp_dir)
                
                # Find hilog directory
                hilog_dir = self._find_hilog_dir(temp_dir)
                if not hilog_dir:
                    logger.error(f"No hilog directory found in {archive_path}")
                    return None
                
                # Process all txt files in hilog dir
                return self._process_directory(hilog_dir)
                
            except patoolib.util.PatoolError as e:
                logger.error(f"Archive extraction failed: {e}")
                return None
    
    def _find_hilog_dir(self, root_dir: str) -> Optional[str]:
        """Recursively search for hilog directory."""
        for root, dirs, _ in os.walk(root_dir):
            if 'hilog' in dirs:
                return os.path.join(root, 'hilog')
        return None
    
    def _process_directory(self, dir_path: str) -> Optional[str]:
        """Process all txt files in a directory."""
        temp_output = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt')
        try:
            for filename in os.listdir(dir_path):
                if filename.endswith('.txt'):
                    filepath = os.path.join(dir_path, filename)
                    self._process_single_file(filepath, output_file=temp_output)
            
            temp_output.close()
            return temp_output.name
            
        except Exception as e:
            logger.error(f"Error processing directory {dir_path}: {e}")
            temp_output.close()
            os.unlink(temp_output.name)
            return None
    
    def _process_single_file(self, file_path: str, output_file=None) -> Optional[str]:
        """Process a single log file with streaming and filtering."""
        # Detect encoding
        encoding = self._detect_encoding(file_path)
        if not encoding:
            return None
        
        # Open output file if not provided
        should_close = False
        if output_file is None:
            output_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt')
            should_close = True
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                self._filter_logs(f, output_file)
                
            if should_close:
                output_file.close()
                return output_file.name
            return None
                
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            if should_close:
                output_file.close()
                os.unlink(output_file.name)
            return None
    
    def _detect_encoding(self, file_path: str) -> Optional[str]:
        """Detect file encoding using chardet."""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Sample first 10KB for detection
                result = chardet.detect(raw_data)
                return result['encoding'] if result['confidence'] > 0.7 else 'utf-8'
        except Exception as e:
            logger.error(f"Encoding detection failed for {file_path}: {e}")
            return None
    
    def _filter_logs(self, input_file, output_file) -> None:
        """Filter logs streaming with context lines capture."""
        context_buffer = []
        
        for line in input_file:
            if self.LOG_PATTERN.search(line) and self.keyword in line:
                # Write context + current line
                output_file.writelines(context_buffer)
                output_file.write(line)
                
                # Capture following context lines
                context_buffer = []
                for _ in range(self.context_lines):
                    next_line = next(input_file, None)
                    if next_line:
                        output_file.write(next_line)
            else:
                # Maintain context buffer (FIFO)
                context_buffer.append(line)
                if len(context_buffer) > self.context_lines:
                    context_buffer.pop(0)