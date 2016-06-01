import unittest

import array
import random
import string
import time

import heatshrink


class EncoderTest(unittest.TestCase):
    def setUp(self):
        self.encoded = heatshrink.encode('abcde')

    def test_encoded_size(self):
        self.assertEqual(self.encoded.shape[0], 6L)

    def test_encoded_bytes(self):
        self.assertEqual(self.encoded.tobytes(), '\xb0\xd8\xacvK(')

    def test_encoded_format(self):
        self.assertEqual(self.encoded.format, 'B')

    def test_encoded_type(self):
        self.assertIsInstance(self.encoded, memoryview)

    def test_encoded_dimensions(self):
        self.assertEqual(self.encoded.ndim, 1)

    def test_encoded_readonly(self):
        self.assertEqual(self.encoded.readonly, True)

    def test_valid_encode_types(self):
        heatshrink.encode('abcde')
        heatshrink.encode(bytes('abcde'))
        heatshrink.encode(unicode('abcde'))
        # TODO: Also get this to work with ByteIO and other
        # TODO: buffer compatible objects.
        # heatshrink.encode(memoryview(b'abcde'))
        # heatshrink.encode(bytearray([1, 2, 3]))
        # heatshrink.encode(array.array('B', [1, 2, 3]))
        with self.assertRaises(TypeError):
            heatshrink.encode([1, 2, 3])
            heatshrink.encode(lambda x: x)
            heatshrink.encode(True)

    def test_encoded_can_be_copied(self):
        copied = self.encoded[:]
        self.assertEqual(copied, self.encoded)
        self.assertIsNot(copied, self.encoded)  # Different identity
        del self.encoded
        # Ensure everything still works
        self.assertEqual(copied.tobytes(), '\xb0\xd8\xacvK(')

    # TODO: Move me to a benchmark
    # def test_encode_large_strings(self):
    #     string_size = 100000
    #     rand_string = ''.join(random.choice(string.lowercase)
    #                           for _ in range(string_size))
    #     start_time = time.time()
    #     # Just test that it doesn't fail
    #     heatshrink.encode(rand_string)
    #     print('\n--- encoded {} bytes in {} seconds ---'
    #           .format(string_size, time.time() - start_time))


class DecoderTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_returns_string(self):
        self.assertIsInstance(heatshrink.decode('abcde'), str)

    def test_accepts_buffer_like_objects(self):
        heatshrink.decode('abcde')
        heatshrink.decode(b'abcde')
        # heatshrink.decode(u'abcde')
        heatshrink.decode(bytearray([1, 2, 3]))
        # heatshrink.decode(array.array('B', [1, 2, 3]))
        heatshrink.decode(memoryview(b'abcde'))
        with self.assertRaisesRegexp(TypeError, ".*buffer protocol.*"):
            heatshrink.decode([1, 2, 3])
            heatshrink.decode(1)
            heatshrink.decode(lambda x: x)
            heatshrink.decode(True)


class EncoderToDecoderTest(unittest.TestCase):
    def test_encoder_output_to_decoder_valid(self):
        encoded = heatshrink.encode(b'a string')
        self.assertEqual(heatshrink.decode(encoded), 'a string')
