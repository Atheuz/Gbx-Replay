import os
import struct
import re
import sys

def uint32(*args):
    return struct.unpack_from('<L', args[0])[0]

def uchar(*args):
    return struct.unpack_from('<B', args[0])[0]

def process_file(*args):
    f = args[0]
    f.seek(0, os.SEEK_SET)
    if f.read(5) == 'GBX' + chr(6) + chr(0):
        f.seek(4, os.SEEK_CUR)
        gbx_type = f.read(4).encode('hex')
        # Replay
        if gbx_type in ['00e00724','00f00324', '00300903']:
            return replay(f), 'replay'
        # Challenge
        elif gbx_type in ['00300024','00300403']:
            return challenge(f), 'challenge'
        else:
            sys.exit('Not an replay or challenge file.')
    else:
        sys.exit('Not an GBX file.')

def replay(*args):
    f = args[0]
    dict_with_info = {}

    # Read header size. uint32
    header_size = uint32(f.read(4))

    # Number of chunks in header. uint32. 1 = TM, 2 = TMPU/TMO/TMS/TMN/TMU/TMF.
    header_chunks = uint32(f.read(4))
    dict_with_info['replay_version'] = header_chunks

    # Determine chunk sizes and positions.
    chunk_offset = 21 + (header_chunks*8)
    string_chunk_size, xml_chunk_size = 0,0
    string_chunk_offset, xml_chunk_offset = 0,0

    for i in range(header_chunks):
        chunk_id = uint32(f.read(4))
        chunk_size = uint32(f.read(4)) & 0x7FFFFFFF

        if chunk_id & 0x00000FFF == 0: # String chunk (TM, VSK)
            string_chunk_id = chunk_id
            string_chunk_size = chunk_size
            string_chunk_offset = chunk_offset
            chunk_offset += chunk_size
        elif chunk_id & 0x00000FFF == 1: # // XML chunk (TM, VSK)
            xml_chunk_id = chunk_id
            xml_chunk_size = chunk_size
            xml_chunk_offset = chunk_offset
            chunk_offset += chunk_size
        else:
            chunk_offset += chunk_size;
            break

    # string chunk
    if string_chunk_size > 4:
        f.seek(string_chunk_offset, os.SEEK_SET)

        dict_with_info['replay_type'] = uint32(f.read(4))

        if dict_with_info['replay_type'] >=2 :
            # Jump to UID size
            f.seek(8, os.SEEK_CUR)

            # Read UID size
            uid_size = uint32(f.read(4))

            # Read UID
            dict_with_info['uid'] = f.read(uid_size)

            f.seek(4, os.SEEK_CUR)
            env_size = uint32(f.read(4))

            # Read Environment
            dict_with_info['environment'] = f.read(env_size)

            # Jump to author name size
            f.seek(4, os.SEEK_CUR)

            # Read author name size
            author_size = uint32(f.read(4))

            # Read author name
            dict_with_info['author_name'] = f.read(author_size)

            # Read replay time
            dict_with_info['replay_time'] = uint32(f.read(4))

            # Read nickname size
            nickname_size = uint32(f.read(4))

            # Read nickname
            nickname = f.read(nickname_size)
            nickname = re.sub('\$[A-F0-9]{1,3}', '', nickname)
            nickname = re.sub('\$[G-Z0-9]{1}', '', nickname)
            nickname = re.sub('\$[a-z0-9]{1,3}', '', nickname)
            dict_with_info['nickname'] = nickname

            if dict_with_info['replay_type'] > 5:
                # Read login size
                login_size = uint32(f.read(4))

                # Read login
                dict_with_info['login'] = f.read(login_size)

    # xml chunk
    if xml_chunk_size > 0:
        # Jump to XML chunk
        f.seek(xml_chunk_offset, os.SEEK_SET)

        # Read xml size
        xml_size = uint32(f.read(4)) & 0x7FFFFFFF

        # Read xml
        dict_with_info['xml'] = f.read(xml_size)

    return dict_with_info


def challenge(*args):
    f = args[0]
    dict_with_info = {}

    # Read header size. uint32.
    header_size = uint32(f.read(4))

    # Number of chunks in header. uint32.
    header_chunks = uint32(f.read(4))
    dict_with_info['challenge_version'] = header_chunks
    if dict_with_info['challenge_version'] not in [2,5,6]:
        return 'Quitting. Challenge version %d not supported' % challenge_version

    # Determine chunk sizes and positions.
    chunk_offset = 21 + (header_chunks*8)
    vehicle_chunk_size, info_chunk_size, string_chunk_size = 0,0,0
    version_chunk_size, xml_chunk_size, thumbnail_chunk_size = 0,0,0
    vehicle_chunk_offset, info_chunk_offset, string_chunk_offset = 0,0,0
    version_chunk_offset, xml_chunk_offset, thumbnail_chunk_offset = 0,0,0

    #for i in range(header_chunks):
    # Only want info and string.
    for i in range(header_chunks):
        # Chunk id. uint32.
        chunk_id = uint32(f.read(4))
        chunk_size = uint32(f.read(4)) & 0x7FFFFFFF
        if chunk_id & 0x00000FFF == 2: # Info chunk (TM only)
            info_chunk_id = chunk_id
            info_chunk_size = chunk_size
            info_chunk_offset = chunk_offset
            chunk_offset += chunk_size
        elif chunk_id & 0x00000FFF == 3: # String chunk (TM, VSK)
            string_chunk_id = chunk_id
            string_chunk_size = chunk_size
            string_chunk_offset = chunk_offset
            chunk_offset += chunk_size
        elif chunk_id & 0x00000FFF == 4: # Version chunk (TM, VSK)
            version_chunk_id = chunk_id
            version_chunk_size = chunk_size
            version_chunk_offset = chunk_offset
            chunk_offset += chunk_size
        elif chunk_id & 0x00000FFF == 5: # XML chunk (TM, VSK)
            xml_chunk_id = chunk_id
            xml_chunk_size = chunk_size
            xml_chunk_offset = chunk_offset
            chunk_offset += chunk_size
        elif chunk_id & 0x00000FFF == 7: # Thumbnail chunk (TM, VSK)
            thumbnail_chunk_id = chunk_id
            thumbnail_chunk_size = chunk_size
            thumbnail_chunk_offset = chunk_offset
            chunk_offset += chunk_size
        elif chunk_id & 0x00000FFF == 1: # // Vehicle chunk (VSK only)
            vehicle_chunk_id = chunk_id
            vehicle_chunk_size = chunk_size
            vehicle_chunk_offset = chunk_offset
            chunk_offset += chunk_size
        else:
            chunk_offset += chunk_size
            break

    # info chunk
    # Go to info chunk and get version
    f.seek(info_chunk_offset, os.SEEK_SET)
    info_version = uchar(f.read(1))

    if info_chunk_size >= 21:
        f.seek(4, os.SEEK_CUR)
        # Bronze Medal time, in milliseconds, or Bronze Stunts score.
        dict_with_info['bronze'] = uint32(f.read(4))
        # INT32: Silver Medal time, in milliseconds, or Silver Stunts score.
        dict_with_info['silver'] = uint32(f.read(4))
        # INT32: Gold Medal time, in milliseconds, or Gold Stunts score.
        dict_with_info['gold'] = uint32(f.read(4))
        # INT32: Author's best time, in milliseconds.
        dict_with_info['author'] = uint32(f.read(4))

        #for i in [bronze,silver,gold,author_time]:
        #    print timedelta(milliseconds=i)

        if info_chunk_size >= 25:
            # INT32: Price of the challenge in coppers.
            dict_with_info['copper_price'] = uint32(f.read(4))
            if info_chunk_size >= 31:
                # 
                # INT32: Multilap flag: 0 if nblaps="0", otherwise 1.
                dict_with_info['multi_lap'] = uint32(f.read(4))
                # INT32: Track type: 0 (Race), 1 (Platform), 2 (Puzzle), 3 (Crazy), 5 (Stunts)
                dict_with_info['track_type'] = uint32(f.read(4))
                if info_chunk_size >= 41:
                    f.seek(4, os.SEEK_CUR)
                    # INT32: Author score/time, or Author Stunts Score.
                    dict_with_info['author_score'] = uint32(f.read(4))

    # string chunk
    if string_chunk_size > 0:
        f.seek(string_chunk_offset, os.SEEK_SET)
        str_version = uchar(f.read(1))

        # Jump to UID size
        f.seek(8, os.SEEK_CUR)

        # Read UID size
        uid_size = uint32(f.read(4))

        # Read UID
        dict_with_info['uid'] = f.read(uid_size)

        f.seek(4, os.SEEK_CUR)
        env_size = uint32(f.read(4))

        # Read Environment
        dict_with_info['environment'] = f.read(env_size)

        # Jump to author name size
        f.seek(4, os.SEEK_CUR)

        # Read author name size
        author_size = uint32(f.read(4))

        # Read author name
        dict_with_info['author_name'] = f.read(author_size)

        # Read track name size
        track_name_size = uint32(f.read(4))

        # Read track name
        dict_with_info['track_name'] = f.read(track_name_size)

        if str_version >= 1:
            # Jump to password size
            f.seek(5, os.SEEK_CUR)

            # Read password size
            password_size = uint32(f.read(4))

            # Read password
            # dict_with_info['password'] = f.read(password_size)
            f.seek(password_size, os.SEEK_CUR)

            if str_version >= 2:
                # Jump to mood size.
                f.seek(4, os.SEEK_CUR)

                # Read mood size
                mood_size = uint32(f.read(4))

                # Read mood name.
                dict_with_info['mood_name'] = f.read(mood_size)

    # version chunk
    f.seek(version_chunk_offset, os.SEEK_SET)

    # Read challenge version
    dict_with_info['challenge_version'] = uint32(f.read(4))

    # xml chunk
    if xml_chunk_size > 0:
        f.seek(xml_chunk_offset, os.SEEK_SET)

        # Read xml size
        xml_size = uint32(f.read(4))

        # Read xml
        dict_with_info['xml'] = f.read(xml_size)

    # thumbnail/comments chunk
    if thumbnail_chunk_size > 0:
        # Jump to thumbnail chunk
        f.seek(thumbnail_chunk_offset, os.SEEK_SET)

        # Check if thumbnail exists
        has_thumbnail = uint32(f.read(4))

        if has_thumbnail != 0:
            # Read thumbnail size
            thumbnail_size = uint32(f.read(4))

            # Jump to thumbnail
            f.seek(15, os.SEEK_CUR)

            # Read thumbnail
            #f.seek(thumbnail_size, os.SEEK_CUR)
            dict_with_info['thumbnail'] = f.read(thumbnail_size)

            # Jump to comments
            f.seek(26, os.SEEK_CUR)

            # Read comments size
            comments_size = uint32(f.read(4))
            if comments_size > 0:
                dict_with_info['comments'] = f.read(comments_size)

    return dict_with_info

