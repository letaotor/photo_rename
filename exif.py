#! /bin/python

import io
import ExifException


class exif:
    exif_subifd = {
        'little': b'\x69\x87',
        'big': b'\x87\x69'
        }
    datetimeoriginal = {
        'little': b'\x03\x90',
        'big': b'\x90\x03'
        }

    def __init__(self, path):
        self.f = io.open(path, 'rb')
        self.exif_subifd_offset = 0
        self.exif_subifd_entry_num = 0
        self.exif_ifd0_entry_num = 0
        self.exif_tag_datetimeoriginal_offset = 0
        self.align = 'unknown'

    def detect_filetype(self):
        filetype = self.f.read(2)
        if filetype == b'\xff\xd8':
            return 'jpg'
        else:
            return 'unknown'

    def detect_app1_marker(self):
        self.f.seek(2, 0)
        app1_marker = self.f.read(2)
        if app1_marker == b'\xff\xe1':
            return True
        else:
            return False

    def detect_exif_header(self):
        self.f.seek(6, 0)
        exif_header = self.f.read(6)
        if exif_header == b'\x45\x78\x69\x66\x00\x00':
            return True
        else:
            return False

    def detect_align(self):
        self.f.seek(12, 0)
        align = self.f.read(2)
        if align == b'\x49\x49':
            self.align = 'little'
        elif align == b'\x4d\x4d':
            self.align = 'big'
        else:
            raise ExifException.UnknownAlign
        return self.align

    def ifd0_num_of_entry(self):
        if self.align == 'unknown':
            self.detect_align()
        self.f.seek(20, 0)
        self.exif_ifd0_entry_num = int.from_bytes(self.f.read(2), self.align)
        return self.ifd0_num_of_entry

    def _exif_subifd_offset(self):
        if self.exif_ifd0_entry_num == 0:
            self.ifd0_num_of_entry()
        if self.align == 'unknown':
            self.detect_align()
        self.f.seek(22, 0)
        for i in range(self.exif_ifd0_entry_num):
            tag = self.f.read(2)
            if tag == self.exif_subifd[self.align]:
                self.f.seek(6, 1)
                self.exif_subifd_offset = \
                    int.from_bytes(self.f.read(4), self.align) + 12
                return self.exif_subifd_offset
            else:
                self.f.seek(10, 1)

    def _exif_tag_datetimeoriginal_offset(self):
        if self.exif_subifd_offset == 0:
            self._exif_subifd_offset()
        self.f.seek(self.exif_subifd_offset, 0)
        subifd_num_of_entry = int.from_bytes(self.f.read(2), self.align)
        for i in range(subifd_num_of_entry):
            tag = self.f.read(2)
            if tag == self.datetimeoriginal[self.align]:
                self.f.seek(6, 1)
                self.exif_tag_datetimeoriginal_offset = \
                    int.from_bytes(self.f.read(4), self.align) + 12
                return self.exif_tag_datetimeoriginal_offset
            else:
                self.f.seek(10, 1)

    def read_tag_datetimeoriginal(self):
        if self.exif_tag_datetimeoriginal_offset == 0:
            self._exif_tag_datetimeoriginal_offset()
        self.f.seek(self.exif_tag_datetimeoriginal_offset, 0)
        return str(self.f.read(19), 'ascii')

    def close(self):
        self.f.close()


if __name__ == "__main__":
    f = exif("./foo.jpg")
    ft = f.detect_filetype()
    align = f.detect_align()
    datetimeoriginal = f.read_tag_datetimeoriginal()
    print("{} {} {}".format(ft, align, datetimeoriginal))
