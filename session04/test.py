import sys

print('Number of arguments:', len(sys.argv),'arguments')
print('Argument List:', str(sys.argv))

sorter, count, order = sys.argv[1:4]

print(sorter, count, order )
