from watermark.watermark import watermark
import concurrent.futures
import threading
import optparse
import shutil
import os
import yaml


MAX_WORKERS=10
parser = optparse.OptionParser()


def get_files(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]


def init_dir(source, destination):

    if os.path.isdir(destination):
        print("Cleaning up destination path")
        shutil.rmtree(destination)

    print("Mirroring source directory tree")
    shutil.copytree(source, destination, ignore=get_files)


def convert_files(source, destination, watermark_file):
    init_dir(source, destination)

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool: 
        for root, _, files in os.walk(source):
            for file in files:
                dst_file = "{0}/{1}".format(root.replace(source, destination), file)
                pool.submit(watermark, "{0}/{1}".format(root, file), dst_file.replace('.pdf',''), watermark_file)
        pool.shutdown(wait=True)


if __name__ == '__main__':
    parser.add_option(
        '-s', '--source',
        action="store", dest="source",
        help="folder where PDFs are located", default="in"
    )
    parser.add_option(
        '-d', '--destination',
        action="store", dest="destination",
        help="destination path where PDFs will be written", default="out"
    )
    parser.add_option(
        '-w', '--watermark',
        action="store", dest="watermark",
        help="watermark PDF that will be applied", default="watermark.pdf"
    )

    options, args = parser.parse_args()
    convert_files(options.source, options.destination, options.watermark)
