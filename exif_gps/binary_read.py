def parse_latitude(offset):
    old_pos = f.tell()
    f.seek(12 + offset)
    print
    for i in xrange(3):
        byte = f.read(4)
        numerator = byte.encode('hex')
        print numerator,

        byte = f.read(4)
        denominator = byte.encode('hex')
        print denominator,
        print int(numerator, 16) / int(denominator, 16)
    print
    print
    f.seek(old_pos)    

def parse_longtitude(offset):
    parse_latitude(offset)

f = open("image.jpg", "rb")
byte = f.read(12)
a = byte.encode('hex')
print a
print

byte = f.read(8)
header_hex = byte.encode('hex')
print header_hex
print

byte = f.read(2)
interoperability_number_hex = byte.encode('hex')
print interoperability_number_hex
print

interoperability_number = int(interoperability_number_hex, 16)
gps_value_offset = 0

for i in xrange(interoperability_number):
    byte = f.read(2)
    tag_id = byte.encode('hex')
    print tag_id,

    byte = f.read(2)
    type_n = byte.encode('hex')
    print type_n,

    byte = f.read(4)
    count = byte.encode('hex')
    print count,

    byte = f.read(4)
    value_offset = byte.encode('hex')
    print value_offset

    if tag_id == '8825':
        print
        gps_value_offset = int(value_offset, 16)
        print gps_value_offset
        print 


# bytes_have_read = 12 + 8 + 2 + 12*interoperability_number 
# print bytes_have_read

f.seek(12 + gps_value_offset)
byte = f.read(2)
a = byte.encode('hex')
print a
print

gps_ifd_number = int(a, 16)

for i in xrange(gps_ifd_number):
    byte = f.read(2)
    tag_id = byte.encode('hex')
    print tag_id,

    byte = f.read(2)
    type_n = byte.encode('hex')
    print type_n,

    byte = f.read(4)
    count = byte.encode('hex')
    print count,

    byte = f.read(4)
    value_offset = byte.encode('hex')
    print value_offset

    if tag_id == '0002':
        parse_latitude(int(value_offset, 16))
    if tag_id == '0004':
        parse_longtitude(int(value_offset, 16))



f.close()




