# This module contains an implementation of a class for encrypting a file with
# a specific cipher in a separate thread.
from app.crypto.common import EncProc
from .widgets import (
    BaseQThread,
    PBarCommands
)


class FileProcessing(BaseQThread):
    def __init__(self, cipher: ..., enc_proc: EncProc, input_file: str, output_file: str,
                 input_file_mode: str, output_file_mode: str, file_size_control: bool = False,
                 read_block_size: int = 1024, control_block_size: int = 8):
        """
        FileProcessing class constructor. This class is designed to encrypt
        a file in a separate stream.

        Args:
            cipher: The cipher with which the file will be encrypted. This cipher
                must have an interface "make".

            enc_proc: parameter responsible for the process of data encryption
                (encryption and decryption).

            input_file: the path to the input file to be encrypted.
            output_file: path to the output file to be written to.
            input_file_mode: a string that contains the mode in which to open the file.
            output_file_mode: a string that contains the mode in which to open the file.
            file_size_control: flag responsible for controlling the file size. Some ciphers
                may add non-significant bytes, which affects integrity. When this flag is enabled,
                it is also worth setting the block size (control_block_size) that will store the file size.
            read_block_size: block size in bytes to be read at a time.
            control_block_size: the size of the block that stores data about the true size of the file.
        """
        super(FileProcessing, self).__init__()
        self._cipher = cipher
        self._enc_proc = enc_proc
        self._input_file = input_file
        self._input_file_mode = input_file_mode
        self._output_file = output_file
        self._output_file_mode = output_file_mode
        self._file_size_control = file_size_control
        self._read_block_size = read_block_size
        self._control_block_size = control_block_size

        self._is_worked = True

    def close(self):
        """Method for stopping a thread"""
        # The flag is set to false and then we start to wait
        # until the loop in the thread stops.
        self._is_worked = False
        self.wait()

    def run(self) -> None:
        """The method that is called after the thread has started via the "start" method"""
        try:
            with open(self._input_file, self._input_file_mode) as input_file, \
                    open(self._output_file, self._output_file_mode) as output_file:
                # Find out the file size (number of bytes - if binary format,
                # number of characters - if normal)
                input_file.seek(0, 2)
                input_file_size = input_file.tell()
                input_file.seek(0, 0)

                # Initializes the progress bar by sending signals to the main window.
                self.pbar.emit((PBarCommands.SET_RANGE, 0, input_file_size))
                self.pbar.emit((PBarCommands.SET_VALUE, 0))
                self.pbar.emit((PBarCommands.SHOW,))

                if self._file_size_control:
                    # If the encryption process, then encrypt the file size with the first block,
                    # if the decryption process, then read the first block - the file size.
                    match self._enc_proc:
                        case EncProc.ENCRYPT:
                            # padding
                            pad = input_file_size.to_bytes(self._control_block_size, "little")
                            encrypted_pad = self._cipher.encrypt(pad)
                            output_file.write(encrypted_pad)

                        case EncProc.DECRYPT:
                            pad = input_file.read(self._control_block_size)
                            decrypted_pad = self._cipher.decrypt(pad)
                            final_file_size = int.from_bytes(decrypted_pad, "little")

                        case _:
                            return

                # We read a piece of data, encrypt it and write it to the output file,
                # simultaneously updating the value in the progress bar.
                while (block := input_file.read(self._read_block_size)) and self._is_worked:
                    processed_block = self._cipher.make(block, self._enc_proc)
                    output_file.write(processed_block)

                    self.pbar.emit((PBarCommands.SET_VALUE, input_file.tell()))

                if self._file_size_control:
                    # If the decryption mode, set the true size of the file.
                    if self._enc_proc is EncProc.DECRYPT:
                        output_file.truncate(final_file_size)

        except Exception as e:
            # If an exception occurs, we send an error message.
            self.message.emit("An error occurred while working with files or when "
                              "determining the file size. (Check encryption mode)\n"
                              f"({e.args[0]})")

        finally:
            # Close the processbar.
            self.pbar.emit((PBarCommands.CLOSE,))
