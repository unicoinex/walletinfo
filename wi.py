#!/usr/bin/env python
#-*- coding: utf-8 -*-

#
# unicoinex's wi.py
# https://github.com/unicoinex/walletinfo.git
# uses code from jackjack-jj which forked from Joric's pywallet.py
# sponsored by coiner8 https://bitcointalk.org/index.php?topic=587012.0
#

__author__ = 'hesham'

coins_list = {0: ["Bitcoin", "BTC",                             # OTHERVERSION: [Name, Code
                  "https://blockchain.info/rawaddr/%s",         # Machine Readable Balance URL
                  "https://blockchain.info/address/%s",         # Human Readable Address Info URL
                  'final_balance":(\d+),', 0.00000001, 128],    # Regex for Machine Readable URL, Multiplier, PrivVersion]
              48: ["Litecoin", "LTC",
                   "http://ltc.blockr.io/api/v1/address/info/%s",
                   "http://ltc.blockr.io/address/info/%s",
                   'balance":([\d.]+),', 1, 176],
              55: ["Peercoin", "PPC",
                   "http://ppc.blockr.io/api/v1/address/info/%s",
                   "http://ppc.blockr.io/address/info/%s",
                   'balance":([\d.]+),', 1, 183],
              30: ["Dogecoin", "DOGE",
                   "https://dogechain.info/chain/Dogecoin/q/addressbalance/%s",
                   "http://dogechain.info/address/%s",
                   '([\d.]+)', 1, 158],
              76: ["Darkcoin", "DRK",
                   "http://explorer.darkcoin.io/chain/DarkCoin/q/addressbalance/%s",
                   "http://explorer.darkcoin.io/address/%s",
                   '([\d.]+)', 1, 204],
              52: ["Namecoin", "NMC",
                   "http://192.241.222.65/chain/Namecoin/q/addressbalance/%s",
                   "http://bitinfocharts.com/namecoin/address/%s",
                   '([\d.]+)', 1, 128],
              25: ["Blackcoin", "BC",
                   "http://blocks.blackcoin.pw/chain/BlackCoin/q/addressbalance/%s",
                   "http://blocks.blackcoin.pw/address/%s",
                   '([\d.]+)', 1, 153],
              56: ["BitShares-PTS", "PTS",
                   "http://ptsexplorer.cloudapp.net/chain/BitShares-PTS/q/addressbalance/%s",
                   "https://coinplorer.com/PTS/Addresses/%s",
                   '([\d.]+)', 1, 184],
              71: ["Vertcoin", "VTC",
                   "https://explorer.vertcoin.org/chain/Vertcoin/q/addressbalance/%s",
                   "https://explorer.vertcoin.org/address/%s",
                   '([\d.]+)', 1, 199],
              58: ["Quark", "QRK",
                   "http://qrk.blockr.io/api/v1/address/info/%s",
                   "http://qrk.blockr.io/address/info/%s",
                   'balance":([\d.]+),', 1, 186],
              23: ["Primecoin", "XPM",
                   "http://xpm.cryptocoinexplorer.com/api/balance/%s",
                   "http://xpm.cryptocoinexplorer.com/address/%s",
                   'balance": ([\d.]+)', 1, 151],
              14: ["Feathercoin", "FTC",
                   "http://ftc.cryptocoinexplorer.com/api/balance/%s",
                   "http://ftc.cryptocoinexplorer.com/address/%s",
                   'balance": ([\d.]+)', 1, 142],
              80: ["Zetacoin", "ZET",
                   "http://darkgamex.ch:2751/chain/ZetaCoin/q/addressbalance/%s",
                   "http://darkgamex.ch:2751/address/%s",
                   'balance": ([\d.]+)', 1, 224],
              50: ["Megacoin", "MEC",
                   "http://mec.blockr.io/api/v1/address/info/%s",
                   "http://mec.blockr.io/address/info/%s",
                   'balance":([\d.]+),', 1, 186],
              8: ["Novacoin", "NVC",
                   "http://nvc.cryptocoinexplorer.com/api/balance/%s",
                   "http://nvc.cryptocoinexplorer.com/address/%s",
                   'balance": ([\d.]+)', 1, 136],
              102: ["Infinitecoin", "IFC",
                   "http://exploretheblocks.com:2750/chain/Infinitecoin/q/addressbalance/%s",
                   "http://exploretheblocks.com:2750/address/%s",
                   '([\d.]+)', 1, 230],
              78: ["YbCoin", "YBC",
                   "http://explorer.ybcoin.com//chain/YbCoin/q/getbalance/%s",
                   "http://explorer.ybcoin.com/address/%s",
                   '([\d.]+)', 1, 206],
              73: ["Worldcoin", "WDC",
                   "http://wdc.cryptocoinexplorer.com/api/balance/%s",
                   "http://wdc.cryptocoinexplorer.com/address/%s",
                   'balance": ([\d.]+)', 1, 201],
              110: ["Maxcoin", "MAX",
                   "http://max.cryptoexplore.com/address/%s",
                   "http://max.cryptoexplore.com/address/%s",
                   'Balance: </td><td>([\d.]+) MAX', 1, 128],
              43: ["Cinnicoin", "CINNI",
                   "http://cinnichain.info/api/address/%s",
                   "http://cinnichain.info/address/%s",
                   'balance":([\d.]+),', 1, 171],
              61: ["Reddcoin", "RDD",
                   "http://cryptexplorer.com/chain/ReddCoin/q/addressbalance/%s",
                   "http://cryptexplorer.com/address/%s",
                   '([\d.]+)', 1, 189],
              68: ["Ultracoin", "UTC",
                   "http://bitgo.pw:3731/chain/Ultracoin/q/addressbalance/%s",
                   "http://bitgo.pw:3731/address/%s",
                   '([\d.]+)', 1, 196],
              51: ["MintCoin", "MNT",
                   "http://mint.blockx.info/get/chain/MintCoin/q/addressbalance/%s",
                   "http://mint.blockx.info/get/address/%s",
                   '([\d.]+)', 1, 179]}

missing_dep = []

try:
    from bsddb.db import *
except:
    try:
        from bsddb3.db import *
    except:
        missing_dep.append('bsddb')

try:
    import json
except:
    try:
        import simplejson as json
    except:
        print("Json or simplejson package is needed")

import logging
import hashlib
import time
import math
import socket
import traceback
import mmap
import struct
import urllib
import random
import os
import re
import tempfile


#TODO this URL should come from the config file
balance_site = 'http://jackjack.alwaysdata.net/balance/index.php?address'

json_db = {}
addrtype = 0
addr_to_keys = {}
passphrase = ""


class AES(object):
    # valid key sizes
    keySize = dict(SIZE_128=16, SIZE_192=24, SIZE_256=32)

    # Rijndael S-box
    sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67,
            0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59,
            0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7,
            0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1,
            0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05,
            0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83,
            0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29,
            0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
            0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa,
            0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c,
            0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc,
            0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
            0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19,
            0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee,
            0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49,
            0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4,
            0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6,
            0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70,
            0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9,
            0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e,
            0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1,
            0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0,
            0x54, 0xbb, 0x16]

    # Rijndael Inverted S-box
    rsbox = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3,
             0x9e, 0x81, 0xf3, 0xd7, 0xfb, 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f,
             0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54,
             0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b,
             0x42, 0xfa, 0xc3, 0x4e, 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24,
             0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, 0x72, 0xf8,
             0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d,
             0x65, 0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda,
             0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84, 0x90, 0xd8, 0xab,
             0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3,
             0x45, 0x06, 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1,
             0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b, 0x3a, 0x91, 0x11, 0x41,
             0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6,
             0x73, 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9,
             0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e, 0x47, 0xf1, 0x1a, 0x71, 0x1d,
             0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
             0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0,
             0xfe, 0x78, 0xcd, 0x5a, 0xf4, 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07,
             0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f, 0x60,
             0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f,
             0x93, 0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5,
             0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2b,
             0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55,
             0x21, 0x0c, 0x7d]

    def getSBoxValue(self, num):
        """Retrieves a given S-Box Value"""
        return self.sbox[num]

    def getSBoxInvert(self, num):
        """Retrieves a given Inverted S-Box Value"""
        return self.rsbox[num]

    def rotate(self, word):
        return word[1:] + word[:1]

    # Rijndael Rcon
    Rcon = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36,
            0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97,
            0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72,
            0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66,
            0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
            0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d,
            0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
            0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61,
            0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
            0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
            0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc,
            0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5,
            0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a,
            0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d,
            0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c,
            0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
            0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4,
            0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
            0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08,
            0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
            0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d,
            0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2,
            0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74,
            0xe8, 0xcb]

    def getRconValue(self, num):
        """Retrieves a given Rcon Value"""
        return self.Rcon[num]

    def core(self, word, iteration):
        """Key schedule core."""
        # rotate the 32-bit word 8 bits to the left
        word = self.rotate(word)
        # apply S-Box substitution on all 4 parts of the 32-bit word
        for i in range(4):
            word[i] = self.getSBoxValue(word[i])
        # XOR the output of the rcon operation with i to the first part
        # (leftmost) only
        word[0] = word[0] ^ self.getRconValue(iteration)
        return word

    def expandKey(self, key, size, expandedKeySize):
        """Rijndael's key expansion.

		Expands an 128,192,256 key into an 176,208,240 bytes key

		expandedKey is a char list of large enough size,
		key is the non-expanded key.
		"""
        # current expanded keySize, in bytes
        currentSize = 0
        rconIteration = 1
        expandedKey = [0] * expandedKeySize

        # set the 16, 24, 32 bytes of the expanded key to the input key
        for j in range(size):
            expandedKey[j] = key[j]
        currentSize += size

        while currentSize < expandedKeySize:
            # assign the previous 4 bytes to the temporary value t
            t = expandedKey[currentSize - 4:currentSize]

            # every 16,24,32 bytes we apply the core schedule to t
            # and increment rconIteration afterwards
            if currentSize % size == 0:
                t = self.core(t, rconIteration)
                rconIteration += 1
            # For 256-bit keys, we add an extra sbox to the calculation
            if size == self.keySize["SIZE_256"] and ((currentSize % size) == 16):
                for l in range(4): t[l] = self.getSBoxValue(t[l])

            # We XOR t with the four-byte block 16,24,32 bytes before the new
            # expanded key.  This becomes the next four bytes in the expanded
            # key.
            for m in range(4):
                expandedKey[currentSize] = expandedKey[currentSize - size] ^ \
                                           t[m]
                currentSize += 1

        return expandedKey

    def addRoundKey(self, state, roundKey):
        """Adds (XORs) the round key to the state."""
        for i in range(16):
            state[i] ^= roundKey[i]
        return state

    def createRoundKey(self, expandedKey, roundKeyPointer):
        """Create a round key.
		Creates a round key from the given expanded key and the
		position within the expanded key.
		"""
        roundKey = [0] * 16
        for i in range(4):
            for j in range(4):
                roundKey[j * 4 + i] = expandedKey[roundKeyPointer + i * 4 + j]
        return roundKey

    def galois_multiplication(self, a, b):
        """Galois multiplication of 8 bit characters a and b."""
        p = 0
        for counter in range(8):
            if b & 1: p ^= a
            hi_bit_set = a & 0x80
            a <<= 1
            # keep a 8 bit
            a &= 0xFF
            if hi_bit_set:
                a ^= 0x1b
            b >>= 1
        return p

    #
    # substitute all the values from the state with the value in the SBox
    # using the state value as index for the SBox
    #
    def subBytes(self, state, isInv):
        if isInv:
            getter = self.getSBoxInvert
        else:
            getter = self.getSBoxValue
        for i in range(16): state[i] = getter(state[i])
        return state

    # iterate over the 4 rows and call shiftRow() with that row
    def shiftRows(self, state, isInv):
        for i in range(4):
            state = self.shiftRow(state, i * 4, i, isInv)
        return state

    # each iteration shifts the row to the left by 1
    def shiftRow(self, state, statePointer, nbr, isInv):
        for i in range(nbr):
            if isInv:
                state[statePointer:statePointer + 4] = \
                    state[statePointer + 3:statePointer + 4] + \
                    state[statePointer:statePointer + 3]
            else:
                state[statePointer:statePointer + 4] = \
                    state[statePointer + 1:statePointer + 4] + \
                    state[statePointer:statePointer + 1]
        return state

    # galois multiplication of the 4x4 matrix
    def mixColumns(self, state, isInv):
        # iterate over the 4 columns
        for i in range(4):
            # construct one column by slicing over the 4 rows
            column = state[i:i + 16:4]
            # apply the mixColumn on one column
            column = self.mixColumn(column, isInv)
            # put the values back into the state
            state[i:i + 16:4] = column

        return state

    # galois multiplication of 1 column of the 4x4 matrix
    def mixColumn(self, column, isInv):
        if isInv:
            mult = [14, 9, 13, 11]
        else:
            mult = [2, 1, 1, 3]
        cpy = list(column)
        g = self.galois_multiplication

        column[0] = g(cpy[0], mult[0]) ^ g(cpy[3], mult[1]) ^ \
                    g(cpy[2], mult[2]) ^ g(cpy[1], mult[3])
        column[1] = g(cpy[1], mult[0]) ^ g(cpy[0], mult[1]) ^ \
                    g(cpy[3], mult[2]) ^ g(cpy[2], mult[3])
        column[2] = g(cpy[2], mult[0]) ^ g(cpy[1], mult[1]) ^ \
                    g(cpy[0], mult[2]) ^ g(cpy[3], mult[3])
        column[3] = g(cpy[3], mult[0]) ^ g(cpy[2], mult[1]) ^ \
                    g(cpy[1], mult[2]) ^ g(cpy[0], mult[3])
        return column

    # applies the 4 operations of the forward round in sequence
    def aes_round(self, state, roundKey):
        state = self.subBytes(state, False)
        state = self.shiftRows(state, False)
        state = self.mixColumns(state, False)
        state = self.addRoundKey(state, roundKey)
        return state

    # applies the 4 operations of the inverse round in sequence
    def aes_invRound(self, state, roundKey):
        state = self.shiftRows(state, True)
        state = self.subBytes(state, True)
        state = self.addRoundKey(state, roundKey)
        state = self.mixColumns(state, True)
        return state

    # Perform the initial operations, the standard round, and the final
    # operations of the forward aes, creating a round key for each round
    def aes_main(self, state, expandedKey, nbrRounds):
        state = self.addRoundKey(state, self.createRoundKey(expandedKey, 0))
        i = 1
        while i < nbrRounds:
            state = self.aes_round(state,
                                   self.createRoundKey(expandedKey, 16 * i))
            i += 1
        state = self.subBytes(state, False)
        state = self.shiftRows(state, False)
        state = self.addRoundKey(state,
                                 self.createRoundKey(expandedKey, 16 * nbrRounds))
        return state

    # Perform the initial operations, the standard round, and the final
    # operations of the inverse aes, creating a round key for each round
    def aes_invMain(self, state, expandedKey, nbrRounds):
        state = self.addRoundKey(state,
                                 self.createRoundKey(expandedKey, 16 * nbrRounds))
        i = nbrRounds - 1
        while i > 0:
            state = self.aes_invRound(state,
                                      self.createRoundKey(expandedKey, 16 * i))
            i -= 1
        state = self.shiftRows(state, True)
        state = self.subBytes(state, True)
        state = self.addRoundKey(state, self.createRoundKey(expandedKey, 0))
        return state

    # encrypts a 128 bit input block against the given key of size specified
    def encrypt(self, iput, key, size):
        output = [0] * 16
        # the number of rounds
        nbrRounds = 0
        # the 128 bit block to encode
        block = [0] * 16
        # set the number of rounds
        if size == self.keySize["SIZE_128"]:
            nbrRounds = 10
        elif size == self.keySize["SIZE_192"]:
            nbrRounds = 12
        elif size == self.keySize["SIZE_256"]:
            nbrRounds = 14
        else:
            return None

        # the expanded keySize
        expandedKeySize = 16 * (nbrRounds + 1)

        # Set the block values, for the block:
        # a0,0 a0,1 a0,2 a0,3
        # a1,0 a1,1 a1,2 a1,3
        # a2,0 a2,1 a2,2 a2,3
        # a3,0 a3,1 a3,2 a3,3
        # the mapping order is a0,0 a1,0 a2,0 a3,0 a0,1 a1,1 ... a2,3 a3,3
        #
        # iterate over the columns
        for i in range(4):
            # iterate over the rows
            for j in range(4):
                block[(i + (j * 4))] = iput[(i * 4) + j]

        # expand the key into an 176, 208, 240 bytes key
        # the expanded key
        expandedKey = self.expandKey(key, size, expandedKeySize)

        # encrypt the block using the expandedKey
        block = self.aes_main(block, expandedKey, nbrRounds)

        # unmap the block again into the output
        for k in range(4):
            # iterate over the rows
            for l in range(4):
                output[(k * 4) + l] = block[(k + (l * 4))]
        return output

    # decrypts a 128 bit input block against the given key of size specified
    def decrypt(self, iput, key, size):
        output = [0] * 16
        # the number of rounds
        nbrRounds = 0
        # the 128 bit block to decode
        block = [0] * 16
        # set the number of rounds
        if size == self.keySize["SIZE_128"]:
            nbrRounds = 10
        elif size == self.keySize["SIZE_192"]:
            nbrRounds = 12
        elif size == self.keySize["SIZE_256"]:
            nbrRounds = 14
        else:
            return None

        # the expanded keySize
        expandedKeySize = 16 * (nbrRounds + 1)

        # Set the block values, for the block:
        # a0,0 a0,1 a0,2 a0,3
        # a1,0 a1,1 a1,2 a1,3
        # a2,0 a2,1 a2,2 a2,3
        # a3,0 a3,1 a3,2 a3,3
        # the mapping order is a0,0 a1,0 a2,0 a3,0 a0,1 a1,1 ... a2,3 a3,3

        # iterate over the columns
        for i in range(4):
            # iterate over the rows
            for j in range(4):
                block[(i + (j * 4))] = iput[(i * 4) + j]
        # expand the key into an 176, 208, 240 bytes key
        expandedKey = self.expandKey(key, size, expandedKeySize)
        # decrypt the block using the expandedKey
        block = self.aes_invMain(block, expandedKey, nbrRounds)
        # unmap the block again into the output
        for k in range(4):
            # iterate over the rows
            for l in range(4):
                output[(k * 4) + l] = block[(k + (l * 4))]
        return output


class AESModeOfOperation(object):
    aes = AES()

    # structure of supported modes of operation
    modeOfOperation = dict(OFB=0, CFB=1, CBC=2)

    # converts a 16 character string into a number array
    def convertString(self, string, start, end, mode):
        if end - start > 16: end = start + 16
        if mode == self.modeOfOperation["CBC"]:
            ar = [0] * 16
        else:
            ar = []

        i = start
        j = 0
        while len(ar) < end - start:
            ar.append(0)
        while i < end:
            ar[j] = ord(string[i])
            j += 1
            i += 1
        return ar

    # Mode of Operation Encryption
    # stringIn - Input String
    # mode - mode of type modeOfOperation
    # hexKey - a hex key of the bit length size
    # size - the bit length of the key
    # hexIV - the 128 bit hex Initilization Vector
    def encrypt(self, stringIn, mode, key, size, IV):
        if len(key) % size:
            return None
        if len(IV) % 16:
            return None
        # the AES input/output
        plaintext = []
        iput = [0] * 16
        output = []
        ciphertext = [0] * 16
        # the output cipher string
        cipherOut = []
        # char firstRound
        firstRound = True
        if stringIn != None:
            for j in range(int(math.ceil(float(len(stringIn)) / 16))):
                start = j * 16
                end = j * 16 + 16
                if end > len(stringIn):
                    end = len(stringIn)
                plaintext = self.convertString(stringIn, start, end, mode)
                # print 'PT@%s:%s' % (j, plaintext)
                if mode == self.modeOfOperation["CFB"]:
                    if firstRound:
                        output = self.aes.encrypt(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes.encrypt(iput, key, size)
                    for i in range(16):
                        if len(plaintext) - 1 < i:
                            ciphertext[i] = 0 ^ output[i]
                        elif len(output) - 1 < i:
                            ciphertext[i] = plaintext[i] ^ 0
                        elif len(plaintext) - 1 < i and len(output) < i:
                            ciphertext[i] = 0 ^ 0
                        else:
                            ciphertext[i] = plaintext[i] ^ output[i]
                    for k in range(end - start):
                        cipherOut.append(ciphertext[k])
                    iput = ciphertext
                elif mode == self.modeOfOperation["OFB"]:
                    if firstRound:
                        output = self.aes.encrypt(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes.encrypt(iput, key, size)
                    for i in range(16):
                        if len(plaintext) - 1 < i:
                            ciphertext[i] = 0 ^ output[i]
                        elif len(output) - 1 < i:
                            ciphertext[i] = plaintext[i] ^ 0
                        elif len(plaintext) - 1 < i and len(output) < i:
                            ciphertext[i] = 0 ^ 0
                        else:
                            ciphertext[i] = plaintext[i] ^ output[i]
                    for k in range(end - start):
                        cipherOut.append(ciphertext[k])
                    iput = output
                elif mode == self.modeOfOperation["CBC"]:
                    for i in range(16):
                        if firstRound:
                            iput[i] = plaintext[i] ^ IV[i]
                        else:
                            iput[i] = plaintext[i] ^ ciphertext[i]
                    # print 'IP@%s:%s' % (j, iput)
                    firstRound = False
                    ciphertext = self.aes.encrypt(iput, key, size)
                    # always 16 bytes because of the padding for CBC
                    for k in range(16):
                        cipherOut.append(ciphertext[k])
        return mode, len(stringIn), cipherOut

    # Mode of Operation Decryption
    # cipherIn - Encrypted String
    # originalsize - The unencrypted string length - required for CBC
    # mode - mode of type modeOfOperation
    # key - a number array of the bit length size
    # size - the bit length of the key
    # IV - the 128 bit number array Initilization Vector
    def decrypt(self, cipherIn, originalsize, mode, key, size, IV):
        # cipherIn = unescCtrlChars(cipherIn)
        if len(key) % size:
            return None
        if len(IV) % 16:
            return None
        # the AES input/output
        ciphertext = []
        iput = []
        output = []
        plaintext = [0] * 16
        # the output plain text string
        stringOut = ''
        # char firstRound
        firstRound = True
        if cipherIn != None:
            for j in range(int(math.ceil(float(len(cipherIn)) / 16))):
                start = j * 16
                end = j * 16 + 16
                if j * 16 + 16 > len(cipherIn):
                    end = len(cipherIn)
                ciphertext = cipherIn[start:end]
                if mode == self.modeOfOperation["CFB"]:
                    if firstRound:
                        output = self.aes.encrypt(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes.encrypt(iput, key, size)
                    for i in range(16):
                        if len(output) - 1 < i:
                            plaintext[i] = 0 ^ ciphertext[i]
                        elif len(ciphertext) - 1 < i:
                            plaintext[i] = output[i] ^ 0
                        elif len(output) - 1 < i and len(ciphertext) < i:
                            plaintext[i] = 0 ^ 0
                        else:
                            plaintext[i] = output[i] ^ ciphertext[i]
                    for k in range(end - start):
                        stringOut += chr(plaintext[k])
                    iput = ciphertext
                elif mode == self.modeOfOperation["OFB"]:
                    if firstRound:
                        output = self.aes.encrypt(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes.encrypt(iput, key, size)
                    for i in range(16):
                        if len(output) - 1 < i:
                            plaintext[i] = 0 ^ ciphertext[i]
                        elif len(ciphertext) - 1 < i:
                            plaintext[i] = output[i] ^ 0
                        elif len(output) - 1 < i and len(ciphertext) < i:
                            plaintext[i] = 0 ^ 0
                        else:
                            plaintext[i] = output[i] ^ ciphertext[i]
                    for k in range(end - start):
                        stringOut += chr(plaintext[k])
                    iput = output
                elif mode == self.modeOfOperation["CBC"]:
                    output = self.aes.decrypt(ciphertext, key, size)
                    for i in range(16):
                        if firstRound:
                            plaintext[i] = IV[i] ^ output[i]
                        else:
                            plaintext[i] = iput[i] ^ output[i]
                    firstRound = False
                    if originalsize is not None and originalsize < end:
                        for k in range(originalsize - start):
                            stringOut += chr(plaintext[k])
                    else:
                        for k in range(end - start):
                            stringOut += chr(plaintext[k])
                    iput = ciphertext
        return stringOut


class BCDataStream(object):
    def __init__(self):
        self.input = None
        self.read_cursor = 0

    def clear(self):
        self.input = None
        self.read_cursor = 0

    def write(self, bytes):  # Initialize with string of bytes
        if self.input is None:
            self.input = bytes
        else:
            self.input += bytes

    def map_file(self, file, start):  # Initialize with bytes from file
        self.input = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
        self.read_cursor = start

    def seek_file(self, position):
        self.read_cursor = position

    def close_file(self):
        self.input.close()

    def read_string(self):
        # Strings are encoded depending on length:
        # 0 to 252 :	1-byte-length followed by bytes (if any)
        # 253 to 65,535 : byte'253' 2-byte-length followed by bytes
        # 65,536 to 4,294,967,295 : byte '254' 4-byte-length followed by bytes
        # ... and the Bitcoin client is coded to understand:
        # greater than 4,294,967,295 : byte '255' 8-byte-length followed by bytes of string
        # ... but I don't think it actually handles any strings that big.
        if self.input is None:
            raise SerializationError("call write(bytes) before trying to deserialize")

        try:
            length = self.read_compact_size()
        except IndexError:
            raise SerializationError("attempt to read past end of buffer")

        return self.read_bytes(length)

    def write_string(self, string):
        # Length-encoded as with read-string
        self.write_compact_size(len(string))
        self.write(string)

    def read_bytes(self, length):
        try:
            result = self.input[self.read_cursor:self.read_cursor + length]
            self.read_cursor += length
            return result
        except IndexError:
            raise SerializationError("attempt to read past end of buffer")

        return ''

    def read_boolean(self):
        return self.read_bytes(1)[0] != chr(0)

    def read_int16(self):
        return self._read_num('<h')

    def read_uint16(self):
        return self._read_num('<H')

    def read_int32(self):
        return self._read_num('<i')

    def read_uint32(self):
        return self._read_num('<I')

    def read_int64(self):
        return self._read_num('<q')

    def read_uint64(self):
        return self._read_num('<Q')

    def write_boolean(self, val):
        return self.write(chr(bool_to_int(val)))

    def write_int16(self, val):
        return self._write_num('<h', val)

    def write_uint16(self, val):
        return self._write_num('<H', val)

    def write_int32(self, val):
        return self._write_num('<i', val)

    def write_uint32(self, val):
        return self._write_num('<I', val)

    def write_int64(self, val):
        return self._write_num('<q', val)

    def write_uint64(self, val):
        return self._write_num('<Q', val)

    def read_compact_size(self):
        size = ord(self.input[self.read_cursor])
        self.read_cursor += 1
        if size == 253:
            size = self._read_num('<H')
        elif size == 254:
            size = self._read_num('<I')
        elif size == 255:
            size = self._read_num('<Q')
        return size

    def write_compact_size(self, size):
        if size < 0:
            raise SerializationError("attempt to write size < 0")
        elif size < 253:
            self.write(chr(size))
        elif size < 2 ** 16:
            self.write('\xfd')
            self._write_num('<H', size)
        elif size < 2 ** 32:
            self.write('\xfe')
            self._write_num('<I', size)
        elif size < 2 ** 64:
            self.write('\xff')
            self._write_num('<Q', size)

    def _read_num(self, format):
        (i,) = struct.unpack_from(format, self.input, self.read_cursor)
        self.read_cursor += struct.calcsize(format)
        return i

    def _write_num(self, format, num):
        s = struct.pack(format, num)
        self.write(s)


class SerializationError(Exception):
    """ Thrown when there's a problem deserializing or serializing """


def bool_to_int(b):
    if b:
        return 1
    return 0


try:
    _p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2FL
except:
    print "Python 3 is not supported, you need Python 2.7.x"
    exit(1)
_r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141L
_b = 0x0000000000000000000000000000000000000000000000000000000000000007L
_a = 0x0000000000000000000000000000000000000000000000000000000000000000L
_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798L
_Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8L

try:
    import ecdsa
    from ecdsa import der

    curve_secp256k1 = ecdsa.ellipticcurve.CurveFp(_p, _a, _b)
    generator_secp256k1 = g = ecdsa.ellipticcurve.Point(curve_secp256k1, _Gx, _Gy, _r)
    randrange = random.SystemRandom().randrange
    secp256k1 = ecdsa.curves.Curve("secp256k1", curve_secp256k1, generator_secp256k1, (1, 3, 132, 0, 10))
    ecdsa.curves.curves.append(secp256k1)
except:
    missing_dep.append('ecdsa')


class CurveFp(object):
    def __init__(self, p, a, b):
        self.__p = p
        self.__a = a
        self.__b = b

    def p(self):
        return self.__p

    def a(self):
        return self.__a

    def b(self):
        return self.__b

    def contains_point(self, x, y):
        return ( y * y - ( x * x * x + self.__a * x + self.__b ) ) % self.__p == 0


class EC_KEY(object):
    def __init__(self, secret):
        curve = CurveFp(_p, _a, _b)
        generator = Point(curve, _Gx, _Gy, _r)
        self.pubkey = Public_key(generator, generator * secret)
        self.privkey = Private_key(self.pubkey, secret)
        self.secret = secret


class Public_key(object):
    def __init__(self, generator, point, c=None):
        self.curve = generator.curve()
        self.generator = generator
        self.point = point
        self.compressed = c
        n = generator.order()
        if not n:
            raise RuntimeError, "Generator point must have order."
        if not n * point == INFINITY:
            raise RuntimeError, "Generator point order is bad."
        if point.x() < 0 or n <= point.x() or point.y() < 0 or n <= point.y():
            raise RuntimeError, "Generator point has x or y out of range."

    def verifies(self, hash, signature):
        G = self.generator
        n = G.order()
        r = signature.r
        s = signature.s
        if r < 1 or r > n - 1: return False
        if s < 1 or s > n - 1: return False
        c = inverse_mod(s, n)
        u1 = ( hash * c ) % n
        u2 = ( r * c ) % n
        xy = u1 * G + u2 * self.point
        v = xy.x() % n
        return v == r

    def ser(self):
        if self.compressed:
            pk = ('%02x' % (2 + (self.point.y() & 1))) + '%064x' % self.point.x()
        else:
            pk = '04%064x%064x' % (self.point.x(), self.point.y())

        return pk.decode('hex')

    def get_addr(self, v=0):
        return public_key_to_bc_address(self.ser(), v)


class Private_key(object):
    def __init__(self, public_key, secret_multiplier):
        self.public_key = public_key
        self.secret_multiplier = secret_multiplier

    def der(self):
        hex_der_key = '06052b8104000a30740201010420' + \
                      '%064x' % self.secret_multiplier + \
                      'a00706052b8104000aa14403420004' + \
                      '%064x' % self.public_key.point.x() + \
                      '%064x' % self.public_key.point.y()
        return hex_der_key.decode('hex')

    def sign(self, hash, random_k):
        G = self.public_key.generator
        n = G.order()
        k = random_k % n
        p1 = k * G
        r = p1.x()
        if r == 0: raise RuntimeError, "amazingly unlucky random number r"
        s = ( inverse_mod(k, n) * ( hash + ( self.secret_multiplier * r ) % n ) ) % n
        if s == 0: raise RuntimeError, "amazingly unlucky random number s"
        return Signature(r, s)


class Signature(object):
    def __init__(self, r, s):
        self.r = r
        self.s = s


class Point(object):
    def __init__(self, curve, x, y, order=None):
        self.__curve = curve
        self.__x = x
        self.__y = y
        self.__order = order
        if self.__curve: assert self.__curve.contains_point(x, y)
        if order: assert self * order == INFINITY

    def __add__(self, other):
        if other == INFINITY: return self
        if self == INFINITY: return other
        assert self.__curve == other.__curve
        if self.__x == other.__x:
            if ( self.__y + other.__y ) % self.__curve.p() == 0:
                return INFINITY
            else:
                return self.double()

        p = self.__curve.p()
        l = ( ( other.__y - self.__y ) * inverse_mod(other.__x - self.__x, p) ) % p
        x3 = ( l * l - self.__x - other.__x) % p
        y3 = ( l * ( self.__x - x3) - self.__y) % p
        return Point(self.__curve, x3, y3)

    def __mul__(self, other):
        def leftmost_bit(x):
            assert x > 0
            result = 1L
            while result <= x: result = 2 * result
            return result / 2

        e = other
        if self.__order: e = e % self.__order
        if e == 0: return INFINITY
        if self == INFINITY: return INFINITY
        assert e > 0
        e3 = 3 * e
        negative_self = Point(self.__curve, self.__x, -self.__y, self.__order)
        i = leftmost_bit(e3) / 2
        result = self
        while i > 1:
            result = result.double()
            if (e3 & i) != 0 and (e & i) == 0: result = result + self
            if (e3 & i) == 0 and (e & i) != 0: result = result + negative_self
            i = i / 2
        return result

    def __rmul__(self, other):
        return self * other

    def __str__(self):
        if self == INFINITY: return "infinity"
        return "(%d,%d)" % ( self.__x, self.__y )

    def double(self):
        if self == INFINITY:
            return INFINITY

        p = self.__curve.p()
        a = self.__curve.a()
        l = ( ( 3 * self.__x * self.__x + a ) * \
              inverse_mod(2 * self.__y, p) ) % p
        x3 = ( l * l - 2 * self.__x ) % p
        y3 = ( l * ( self.__x - x3 ) - self.__y ) % p
        return Point(self.__curve, x3, y3)

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def curve(self):
        return self.__curve

    def order(self):
        return self.__order


INFINITY = Point(None, None, None)


def inverse_mod(a, m):
    if a < 0 or m <= a: a = a % m
    c, d = a, m
    uc, vc, ud, vd = 1, 0, 0, 1
    while c != 0:
        q, c, d = divmod(d, c) + (c, )
        uc, vc, ud, vd = ud - q * uc, vd - q * vc, uc, vc
    assert d == 1
    if ud > 0:
        return ud
    else:
        return ud + m


###################################
# pywallet crypter implementation #
###################################

crypter = None

try:
    from Crypto.Cipher import AES

    crypter = 'pycrypto'
except:
    pass


class Crypter_pycrypto(object):
    def SetKeyFromPassphrase(self, vKeyData, vSalt, nDerivIterations, nDerivationMethod):
        if nDerivationMethod != 0:
            return 0
        data = vKeyData + vSalt
        for i in xrange(nDerivIterations):
            data = hashlib.sha512(data).digest()
        self.SetKey(data[0:32])
        self.SetIV(data[32:32 + 16])
        return len(data)

    def SetKey(self, key):
        self.chKey = key

    def SetIV(self, iv):
        self.chIV = iv[0:16]

    def Encrypt(self, data):
        return AES.new(self.chKey, AES.MODE_CBC, self.chIV).encrypt(data)[0:32]

    def Decrypt(self, data):
        return AES.new(self.chKey, AES.MODE_CBC, self.chIV).decrypt(data)[0:32]


class Crypter_pure(object):
    def __init__(self):
        self.m = AESModeOfOperation()
        self.cbc = self.m.modeOfOperation["CBC"]
        self.sz = self.m.aes.keySize["SIZE_256"]

    def SetKeyFromPassphrase(self, vKeyData, vSalt, nDerivIterations, nDerivationMethod):
        if nDerivationMethod != 0:
            return 0
        data = vKeyData + vSalt
        for i in xrange(nDerivIterations):
            data = hashlib.sha512(data).digest()
        self.SetKey(data[0:32])
        self.SetIV(data[32:32 + 16])
        return len(data)

    def SetKey(self, key):
        self.chKey = [ord(i) for i in key]

    def SetIV(self, iv):
        self.chIV = [ord(i) for i in iv]

    def Encrypt(self, data):
        mode, size, cypher = self.m.encrypt(data, self.cbc, self.chKey, self.sz, self.chIV)
        return ''.join(map(chr, cypher))

    def Decrypt(self, data):
        chData = [ord(i) for i in data]
        return self.m.decrypt(chData, self.sz, self.cbc, self.chKey, self.sz, self.chIV)


if crypter == 'pycrypto':
    crypter = Crypter_pycrypto()
else:
    crypter = Crypter_pure()
    logging.warning("pycrypto not found, decryption may be slow")

##########################################
# end of pywallet crypter implementation #
##########################################


def read_wallet(json_db, walletfile, print_wallet, print_wallet_transactions, transaction_filter,
                include_balance, test_passphrase=False, vers=-1):
    global passphrase, addr_to_keys
    crypted = False

    private_keys = []
    private_hex_keys = []

    if vers > -1:
        global addrtype
        oldaddrtype = addrtype
        addrtype = vers

    db = open_wallet(walletfile)

    json_db['keys'] = []
    json_db['pool'] = []
    json_db['tx'] = []
    json_db['names'] = {}
    json_db['ckey'] = []
    json_db['mkey'] = {}

    def item_callback(type, d):
        if type == "tx":
            json_db['tx'].append(
                {"tx_id": d['tx_id'], "txin": d['txIn'], "txout": d['txOut'], "tx_v": d['txv'], "tx_k": d['txk']})

        elif type == "name":
            json_db['names'][d['hash']] = d['name']

        elif type == "version":
            json_db['version'] = d['version']

        elif type == "minversion":
            json_db['minversion'] = d['minversion']

        elif type == "setting":
            if not json_db.has_key('settings'): json_db['settings'] = {}
            json_db["settings"][d['setting']] = d['value']

        elif type == "defaultkey":
            json_db['defaultkey'] = public_key_to_bc_address(d['key'])

        elif type == "key":
            addr = public_key_to_bc_address(d['public_key'])
            compressed = d['public_key'][0] != '\04'
            sec = SecretToASecret(PrivKeyToSecret(d['private_key']), compressed)
            hexsec = ASecretToSecret(sec).encode('hex')[:32]
            private_keys.append(sec)
            addr_to_keys[addr] = [hexsec, d['public_key'].encode('hex')]
            json_db['keys'].append(
                {'addr': addr, 'sec': sec, 'hexsec': hexsec, 'secret': hexsec, 'pubkey': d['public_key'].encode('hex'),
                 'compressed': compressed, 'private': d['private_key'].encode('hex')})

        elif type == "wkey":
            if not json_db.has_key('wkey'): json_db['wkey'] = []
            json_db['wkey']['created'] = d['created']

        elif type == "pool":
            try:
                json_db['pool'].append({'n': d['n'], 'addr': public_key_to_bc_address(d['public_key']),
                                        'addr2': public_key_to_bc_address(d['public_key'].decode('hex')),
                                        'addr3': public_key_to_bc_address(d['public_key'].encode('hex')),
                                        'nTime': d['nTime'], 'nVersion': d['nVersion'],
                                        'public_key_hex': d['public_key']})
            except:
                json_db['pool'].append(
                    {'n': d['n'], 'addr': public_key_to_bc_address(d['public_key']), 'nTime': d['nTime'],
                     'nVersion': d['nVersion'], 'public_key_hex': d['public_key'].encode('hex')})

        elif type == "acc":
            json_db['acc'] = d['account']
            # print("Account %s (current key: %s)" % (d['account'], public_key_to_bc_address(d['public_key'])))

        elif type == "acentry":
            json_db['acentry'] = (
                d['account'], d['nCreditDebit'], d['otherAccount'], time.ctime(d['nTime']), d['n'], d['comment'])

        elif type == "bestblock":
            json_db['bestblock'] = d['hashes'][0][::-1].encode('hex_codec')

        elif type == "ckey":
            crypted = True
            compressed = d['public_key'][0] != '\04'
            json_db['keys'].append(
                {'pubkey': d['public_key'].encode('hex'), 'addr': public_key_to_bc_address(d['public_key']),
                 'encrypted_privkey': d['encrypted_private_key'].encode('hex_codec'), 'compressed': compressed})

        elif type == "mkey":
            json_db['mkey']['nID'] = d['nID']
            json_db['mkey']['encrypted_key'] = d['encrypted_key'].encode('hex_codec')
            json_db['mkey']['salt'] = d['salt'].encode('hex_codec')
            json_db['mkey']['nDerivationMethod'] = d['nDerivationMethod']
            json_db['mkey']['nDerivationIterations'] = d['nDerivationIterations']
            json_db['mkey']['otherParams'] = d['otherParams']

            if passphrase:
                res = crypter.SetKeyFromPassphrase(passphrase, d['salt'], d['nDerivationIterations'],
                                                   d['nDerivationMethod'])
                if res == 0:
                    logging.error("Unsupported derivation method")
                    sys.exit(1)
                masterkey = crypter.Decrypt(d['encrypted_key'])
                crypter.SetKey(masterkey)

        else:
            json_db[type] = 'unsupported'
            #print "Wallet data not recognized: " + str(d)

    list_of_reserve_not_in_pool = []
    parse_wallet(db, item_callback)

    nkeys = len(json_db['keys'])
    i = 0
    for k in json_db['keys']:
        i += 1
        addr = k['addr']

        if addr in json_db['names'].keys():
            k["label"] = json_db['names'][addr]
            k["reserve"] = 0
        else:
            k["reserve"] = 1
            list_of_reserve_not_in_pool.append(k['pubkey'])


    def rnip_callback(a):
        list_of_reserve_not_in_pool.remove(a['public_key_hex'])


    db.close()

    crypted = 'salt' in json_db['mkey']

    if not crypted and test_passphrase:
        print "Unencrypted"
        exit(0)

    if crypted and not passphrase and test_passphrase:
        print "Incorrect"
        exit(1)

    if crypted and passphrase:
        check = True
        ppcorrect = True
        for k in json_db['keys']:
            if 'encrypted_privkey' in k:
                ckey = k['encrypted_privkey'].decode('hex')
                public_key = k['pubkey'].decode('hex')
                crypter.SetIV(Hash(public_key))
                secret = crypter.Decrypt(ckey)
                compressed = public_key[0] != '\04'

                if check:
                    check = False
                    pkey = EC_KEY(int('0x' + secret.encode('hex'), 16))
                    if public_key != GetPubKey(pkey, compressed):
                        ppcorrect = False
                    elif public_key == GetPubKey(pkey, compressed):
                        ppcorrect = True

                if test_passphrase and not ppcorrect:
                    print "Incorrect"
                    exit(1)
                elif test_passphrase and ppcorrect:
                    print "Correct"
                    exit(0)
                elif not ppcorrect:
                    print "Incorrect passphrase! Exiting"
                    exit(1)

                sec = SecretToASecret(secret, compressed)
                k['sec'] = sec
                k['hexsec'] = secret[:32].encode('hex')
                k['secret'] = secret.encode('hex')
                k['compressed'] = compressed
                addr_to_keys[k['addr']] = [sec, k['pubkey']]
                #			del(k['ckey'])
                #			del(k['secret'])
                #			del(k['pubkey'])
                private_keys.append(sec)

    for k in json_db['keys']:
        if k['compressed'] and 'secret' in k:
            k['secret'] += "01"

    if vers > -1:
        addrtype = oldaddrtype

    return crypted


def open_wallet(walletfile):
    db = DB()

    flags = DB_THREAD | DB_RDONLY
    # noinspection PyUnresolvedReferences
    try:
        r = db.open(walletfile, "main", DB_BTREE, flags)
    except DBError:
        r = True

    if r is not None:
        logging.error("Couldn't open wallet.dat/main. Are you sure you are using the right datadir?")
        sys.exit(1)

    return db


def hash_160(public_key):
    md = hashlib.new('ripemd160')
    md.update(hashlib.sha256(public_key).digest())
    return md.digest()


def public_key_to_bc_address(public_key, v=None):
    if v == None:
        v = addrtype
    h160 = hash_160(public_key)
    return hash_160_to_bc_address(h160, v)


def hash_160_to_bc_address(h160, v=None):
    if v == None:
        v = addrtype
    vh160 = chr(v) + h160
    h = Hash(vh160)
    addr = vh160 + h[0:4]
    return b58encode(addr)


__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)


def b58encode(v):
    """ encode v, which is a string of bytes, to base58.
	"""

    long_value = 0L
    for (i, c) in enumerate(v[::-1]):
        long_value += (256 ** i) * ord(c)

    result = ''
    while long_value >= __b58base:
        div, mod = divmod(long_value, __b58base)
        result = __b58chars[mod] + result
        long_value = div
    result = __b58chars[long_value] + result

    # Bitcoin does a little leading-zero-compression:
    # leading 0-bytes in the input become leading-1s
    nPad = 0
    for c in v:
        if c == '\0':
            nPad += 1
        else:
            break

    return (__b58chars[0] * nPad) + result


def b58decode(v, length):
    long_value = 0L
    for (i, c) in enumerate(v[::-1]):
        long_value += __b58chars.find(c) * (__b58base ** i)

    result = ''
    while long_value >= 256:
        div, mod = divmod(long_value, 256)
        result = chr(mod) + result
        long_value = div
    result = chr(long_value) + result

    nPad = 0
    for c in v:
        if c == __b58chars[0]:
            nPad += 1
        else:
            break

    result = chr(0) * nPad + result
    if length is not None and len(result) != length:
        return None

    return result


def Hash(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def SecretToASecret(secret, compressed=False):
    prefix = chr(coins_list[addrtype][6])
    vchIn = prefix + secret
    if compressed: vchIn += '\01'
    return EncodeBase58Check(vchIn)


def EncodeBase58Check(secret):
    hash = Hash(secret)
    return b58encode(secret + hash[0:4])


def DecodeBase58Check(sec):
    vchRet = b58decode(sec, None)
    secret = vchRet[0:-4]
    csum = vchRet[-4:]
    hash = Hash(secret)
    cs32 = hash[0:4]
    if cs32 != csum:
        return None
    else:
        return secret


def PrivKeyToSecret(privkey):
    if len(privkey) == 279:
        return privkey[9:9 + 32]
    else:
        return privkey[8:8 + 32]


def ASecretToSecret(sec):
    vch = DecodeBase58Check(sec)
    if not vch:
        return False
    return vch[1:]


def parse_wallet(db, item_callback):
    kds = BCDataStream()
    vds = BCDataStream()

    def parse_TxIn(vds):
        d = {}
        d['prevout_hash'] = vds.read_bytes(32).encode('hex')
        d['prevout_n'] = vds.read_uint32()
        d['scriptSig'] = vds.read_bytes(vds.read_compact_size()).encode('hex')
        d['sequence'] = vds.read_uint32()
        return d

    def parse_TxOut(vds):
        d = {}
        d['value'] = vds.read_int64() / 1e8
        d['scriptPubKey'] = vds.read_bytes(vds.read_compact_size()).encode('hex')
        return d

    for (key, value) in db.items():
        d = {}
        kds.clear()
        kds.write(key)
        vds.clear()
        vds.write(key)

        type = kds.read_string()

        d["__key__"] = key
        d["__value__"] = value
        d["__type__"] = type

        try:
            if type == "name":
                d['hash'] = kds.read_string()
                d['name'] = vds.read_string()
                global addrtype
                addrtype = get_addrtype(d['hash'])
                if addrtype not in coins_list:
                    print "Wallet coin undefined/unsupported. Otherversion: " + str(addrtype)
                    exit(1)
                break

        except Exception, e:
            traceback.print_exc()
            print("ERROR parsing wallet.dat, type %s" % type)
            print("key data: %s" % key)
            print("key data in hex: %s" % key.encode('hex_codec'))
            print("value data in hex: %s" % value.encode('hex_codec'))
            sys.exit(1)

    for (key, value) in db.items():
        d = {}

        kds.clear()
        kds.write(key)
        vds.clear()
        vds.write(value)

        type = kds.read_string()

        d["__key__"] = key
        d["__value__"] = value
        d["__type__"] = type

        try:
            if type == "tx":
                d["tx_id"] = inversetxid(kds.read_bytes(32).encode('hex_codec'))
                start = vds.read_cursor
                d['version'] = vds.read_int32()
                n_vin = vds.read_compact_size()
                d['txIn'] = []
                for i in xrange(n_vin):
                    d['txIn'].append(parse_TxIn(vds))
                n_vout = vds.read_compact_size()
                d['txOut'] = []
                for i in xrange(n_vout):
                    d['txOut'].append(parse_TxOut(vds))
                d['lockTime'] = vds.read_uint32()
                d['tx'] = vds.input[start:vds.read_cursor].encode('hex_codec')
                d['txv'] = value.encode('hex_codec')
                d['txk'] = key.encode('hex_codec')
            elif type == "name":
                d['hash'] = kds.read_string()
                d['name'] = vds.read_string()
            elif type == "version":
                d['version'] = vds.read_uint32()
            elif type == "minversion":
                d['minversion'] = vds.read_uint32()
            elif type == "setting":
                d['setting'] = kds.read_string()
                d['value'] = parse_setting(d['setting'], vds)
            elif type == "key":
                d['public_key'] = kds.read_bytes(kds.read_compact_size())
                d['private_key'] = vds.read_bytes(vds.read_compact_size())
            elif type == "wkey":
                d['public_key'] = kds.read_bytes(kds.read_compact_size())
                d['private_key'] = vds.read_bytes(vds.read_compact_size())
                d['created'] = vds.read_int64()
                d['expires'] = vds.read_int64()
                d['comment'] = vds.read_string()
            elif type == "defaultkey":
                d['key'] = vds.read_bytes(vds.read_compact_size())
            elif type == "pool":
                d['n'] = kds.read_int64()
                d['nVersion'] = vds.read_int32()
                d['nTime'] = vds.read_int64()
                d['public_key'] = vds.read_bytes(vds.read_compact_size())
            elif type == "acc":
                d['account'] = kds.read_string()
                d['nVersion'] = vds.read_int32()
                d['public_key'] = vds.read_bytes(vds.read_compact_size())
            elif type == "acentry":
                d['account'] = kds.read_string()
                d['n'] = kds.read_uint64()
                d['nVersion'] = vds.read_int32()
                d['nCreditDebit'] = vds.read_int64()
                d['nTime'] = vds.read_int64()
                d['otherAccount'] = vds.read_string()
                d['comment'] = vds.read_string()
            elif type == "bestblock":
                d['nVersion'] = vds.read_int32()
                d.update(parse_BlockLocator(vds))
            elif type == "ckey":
                d['public_key'] = kds.read_bytes(kds.read_compact_size())
                d['encrypted_private_key'] = vds.read_bytes(vds.read_compact_size())
            elif type == "mkey":
                d['nID'] = kds.read_uint32()
                d['encrypted_key'] = vds.read_string()
                d['salt'] = vds.read_string()
                d['nDerivationMethod'] = vds.read_uint32()
                d['nDerivationIterations'] = vds.read_uint32()
                d['otherParams'] = vds.read_string()

            item_callback(type, d)

        except Exception, e:
            traceback.print_exc()
            print("ERROR parsing wallet.dat, type %s" % type)
            print("key data: %s" % key)
            print("key data in hex: %s" % key.encode('hex_codec'))
            print("value data in hex: %s" % value.encode('hex_codec'))
            sys.exit(1)


def inversetxid(txid):
    if len(txid) is not 64:
        print("Bad txid")
        return "CORRUPTEDTXID:" + txid
    #		exit(0)
    new_txid = ""
    for i in range(32):
        new_txid += txid[62 - 2 * i];
        new_txid += txid[62 - 2 * i + 1];
    return new_txid


def parse_setting(setting, vds):
    if setting[0] == "f":  # flag (boolean) settings
        return str(vds.read_boolean())
    elif setting[0:4] == "addr":  # CAddress
        d = parse_CAddress(vds)
        return deserialize_CAddress(d)
    elif setting == "nTransactionFee":
        return vds.read_int64()
    elif setting == "nLimitProcessors":
        return vds.read_int32()
    return 'unknown setting'


def parse_CAddress(vds):
    d = {'ip': '0.0.0.0', 'port': 0, 'nTime': 0}
    try:
        d['nVersion'] = vds.read_int32()
        d['nTime'] = vds.read_uint32()
        d['nServices'] = vds.read_uint64()
        d['pchReserved'] = vds.read_bytes(12)
        d['ip'] = socket.inet_ntoa(vds.read_bytes(4))
        d['port'] = vds.read_uint16()
    except:
        pass
    return d


def deserialize_CAddress(d):
    return d['ip'] + ":" + str(d['port'])


def parse_BlockLocator(vds):
    d = {'hashes': []}
    nHashes = vds.read_compact_size()
    for i in xrange(nHashes):
        d['hashes'].append(vds.read_bytes(32))
        return d


def print_balances(json_db):
    for k in json_db['keys']:
        if k:
            site = coins_list[addrtype][2] % k['addr']
            response = urllib.urlopen(site)
            page = response.read()
            m = re.search(coins_list[addrtype][4], page)
            if m:
                print k['addr'] + "," + str(float(m.group(1)) * coins_list[addrtype][5])
            else:
                print "Error reading balance for address: " + k['addr']


def test_print_balance(addr, code):
    site = coins_list[code][2] % addr
    response = urllib.urlopen(site)
    page = response.read()
    m = re.search(coins_list[code][4], page)
    print addr + "," + str(float(m.group(1)) * coins_list[code][5])


def GetPubKey(pkey, compressed=False):
    return i2o_ECPublicKey(pkey, compressed)


def i2o_ECPublicKey(pkey, compressed=False):
    # public keys are 65 bytes long (520 bits)
    # 0x04 + 32-byte X-coordinate + 32-byte Y-coordinate
    # 0x00 = point at infinity, 0x02 and 0x03 = compressed, 0x04 = uncompressed
    # compressed keys: <sign> <x> where <sign> is 0x02 if y is even and 0x03 if y is odd
    if compressed:
        if pkey.pubkey.point.y() & 1:
            key = '03' + '%064x' % pkey.pubkey.point.x()
        else:
            key = '02' + '%064x' % pkey.pubkey.point.x()
    else:
        key = '04' + \
              '%064x' % pkey.pubkey.point.x() + \
              '%064x' % pkey.pubkey.point.y()

    return key.decode('hex')


def print_keys(json_db, print_public=True, print_private=True):
    for k in json_db['keys']:
        if k:
            if print_public and print_private:
                print k['addr'] + "," + k['sec']
            elif print_private:
                print k['sec']
            elif print_public:
                print k['addr']


def print_names(json_db):
    for n in json_db['names']:
        if n:
            print n + "," + '"' + json_db['names'][n] + '"'


def print_coin_type():
    print coins_list[addrtype][1] + "," + str(addrtype)


def print_explore_urls(json_db):
    for k in json_db['keys']:
        if k:
            print coins_list[addrtype][3] % k['addr']


def get_addrtype(v):
    return ord(DecodeBase58Check(v)[0])


from optparse import OptionParser


if __name__ == '__main__':

    prog = os.path.basename(__file__)

    parser = OptionParser(usage="%prog [options]", version="%prog 1.0")

    parser.add_option("--wallet", dest="walletfile",
                      help="full path to wallet (defaults to ./wallet.dat)",
                      default="./wallet.dat")

    parser.add_option("--is-encrypted", dest="check_encryption", action="store_true",
                      help="check if wallet is encrypted")

    parser.add_option("--passphrase", dest="passphrase",
                      help="passphrase for the encrypted wallet")

    parser.add_option("--test-passphrase", dest="test_passphrase", action="store_true",
                      help="test if passed passphrase is correct")

    parser.add_option("--determine-coin", dest="determine_coin", action="store_true",
                      help="tries to determine coin")

    parser.add_option("--list-keys", dest="list_keys", action="store_true",
                      help="list private and public keys")

    parser.add_option("--list-public-keys", dest="list_public_keys", action="store_true",
                      help="list only public keys")

    parser.add_option("--list-private-keys", dest="list_private_keys", action="store_true",
                      help="list only private keys")

    parser.add_option("--list-contacts", dest="list_contacts", action="store_true",
                      help="lists wallet address book contacts")

    parser.add_option("--balances", dest="list_balances", action="store_true",
                      help="list balances for each key")

    parser.add_option("--explorer-url", dest="list_explore_url", action="store_true",
                      help="print block explorer url for each address")

    (options, args) = parser.parse_args()

    if options.passphrase:
        passphrase = options.passphrase

    if 'bsddb' in missing_dep:
        print("%s needs 'bsddb' package to run, please install it" % prog)
        exit(0)

    if 'ecdsa' in missing_dep:
        print("%s needs 'ecdsa' package to run, please install it" % prog)
        exit(0)

    db_dir = os.path.dirname(options.walletfile)
    wallet_file = os.path.basename(options.walletfile)
    #db_env = create_env(db_dir)

    if not options.check_encryption and not options.test_passphrase and not options.determine_coin \
            and not options.list_keys and not options.list_public_keys and not options.list_private_keys \
            and not options.list_contacts and not options.list_balances and not options.list_explore_url:
        print("Nothing to do! For help run '%s --help'" % prog)
        exit(0)

    encrypted = read_wallet(json_db, options.walletfile, True, True, "", False, options.test_passphrase)

    if options.check_encryption:
        if encrypted:
            print "Encrypted"
        else:
            print "Unencrypted"
        exit(0)

    if options.list_keys:
        if encrypted and not passphrase:
            print "Can't print public and private keys for encrypted wallet without passphrase!"
            exit(1)
        print_keys(json_db)
        exit(0)

    if options.list_private_keys:
        if encrypted and not passphrase:
            print "Can't print private keys for encrypted wallet without passphrase!"
            exit(1)
        print_keys(json_db, False, True)
        exit(0)

    if options.list_public_keys:
        print_keys(json_db, True, False)
        exit(0)

    if options.list_contacts:
        print_names(json_db)
        exit(0)

    if options.list_balances:
        print_balances(json_db)
        exit(0)

    if options.list_explore_url:
        print print_explore_urls(json_db)
        exit(0)

    if options.determine_coin:
        print_coin_type()
        exit(0)
