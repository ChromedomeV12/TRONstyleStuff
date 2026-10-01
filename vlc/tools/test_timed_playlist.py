import csv
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
from make_timed_playlist import build,seconds,VLC,XSPF

class TimedPlaylistTests(unittest.TestCase):
    def test_clock_times(self):
        self.assertEqual(seconds('1:02.5'),62.5)
        self.assertEqual(seconds('1:02:03'),3723)
        for bad in ('-1','NaN','inf','1:60','1::2','1.5:20'):
            with self.subTest(bad=bad),self.assertRaises(ValueError):seconds(bad)

    def test_unicode_paths_and_xml_escaping(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);media=folder/'music & 音乐.wav';media.write_bytes(b'test')
            source=folder/'tracks.csv'
            with source.open('w',encoding='utf-8',newline='') as stream:
                writer=csv.writer(stream);writer.writerow(['file','start','stop','title'])
                writer.writerow([media.name,'0:12','1:42','A & B <mix>'])
            root=ET.fromstring(build(source))
            self.assertEqual(root.find('.//{'+XSPF+'}location').text,media.as_uri())
            self.assertEqual(root.find('.//{'+XSPF+'}track/{'+XSPF+'}title').text,'A & B <mix>')
            self.assertEqual([e.text for e in root.iter('{'+VLC+'}option')],['start-time=12','stop-time=102'])
            source.write_text('file,start,stop\n'+media.name+',10,9\n',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'Stop must be later'):build(source)
            source.write_text('file,start,stop\nmissing.wav,0,2\n',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'not found'):build(source)

if __name__=='__main__':unittest.main()
