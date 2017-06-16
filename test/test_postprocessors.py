#!/usr/bin/env python

from __future__ import unicode_literals

# Allow direct execution
import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test.helper import (
    FakeYDL,
)

from youtube_dl.postprocessor import MetadataFromTitlePP

class TestMetadataFromTitle(unittest.TestCase):
    def test_format_to_regex(self):
        pp = MetadataFromTitlePP(None, '%(title)s - %(artist)s')
        self.assertEqual(pp._titleregex, '(?P<title>.+)\ \-\ (?P<artist>.+)')

    def test_regex_captures(self):
        postprocessor = MetadataFromTitlePP(FakeYDL(), '^(?P<track_number>\d+) - (?P<track>.+?)(?: - (?P<artist>.+?))?(?: - (?P<album>.+?))??(?: \((?P<comment>.+?)\))?$')

        info = {'title':'1 - Orinoco Flow - Enya - Jenny\'s Dank AF Roadtrip Jamz (that shit\'s fire)'}
        postprocessor.run(info)
        self.assertEqual(info['track_number'], '1')
        self.assertEqual(info['track'], 'Orinoco Flow')
        self.assertEqual(info['artist'], 'Enya')
        self.assertEqual(info['album'], 'Jenny\'s Dank AF Roadtrip Jamz')
        self.assertEqual(info['comment'], 'that shit\'s fire')

        info = {'title':'02 - Time After Time - Cindi Lauper - Jenny\'s Dank AF Roadtrip Jamz'}
        postprocessor.run(info)
        self.assertEqual(info['track_number'], '02')
        self.assertEqual(info['track'], 'Time After Time')
        self.assertEqual(info['artist'], 'Cindi Lauper')
        self.assertEqual(info['album'], 'Jenny\'s Dank AF Roadtrip Jamz')
        self.assertNotIn('comment', info)

        info = {'title':'9000 - Always - Erasure'}
        postprocessor.run(info)
        self.assertEqual(info['track_number'], '9000')
        self.assertEqual(info['track'], 'Always')
        self.assertEqual(info['artist'], 'Erasure')
        self.assertNotIn('album', info)
        self.assertNotIn('comment', info)

        info = {'title':'99 - Jenny burps "99 Problems" by Jay Z'}
        postprocessor.run(info)
        self.assertEqual(info['track_number'], '99')
        self.assertEqual(info['track'], 'Jenny burps "99 Problems" by Jay Z')
        self.assertNotIn('artist', info)
        self.assertNotIn('album', info)
        self.assertNotIn('comment', info)

if __name__ == '__main__':
    unittest.main()
