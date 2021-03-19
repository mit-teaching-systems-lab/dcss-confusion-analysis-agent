import argparse, os, random, re, shutil, sys
import urllib.parse
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--token", help="The X-DCSS-MEDIA-REQUEST-TOKEN")
parser.add_argument("-u", "--url", help="The URL of the media file to request")

def classify(filename):
	# Just some non-sense to make this do "something"
	return bool(random.getrandbits(1))

def makeHeaders(token):
	return {'X-DCSS-MEDIA-REQUEST-TOKEN': token}

def main():
	args = parser.parse_args()

	if args.token == '':
		sys.exit('--token is empty')

	if args.url == '':
		sys.exit('--url is empty')

	urlparts = urllib.parse.urlsplit(args.url)
	save_path = './media/' + os.path.basename(urlparts.path)

	request = urllib.request.Request(args.url, headers=makeHeaders(args.token))
	with urllib.request.urlopen(request) as response, open(save_path, 'wb') as out_file:
			shutil.copyfileobj(response, out_file)

	sys.stdout.write(str(classify(save_path)))


if __name__ == "__main__":
	main()
