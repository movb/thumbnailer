from thumbnail import generate_thumb
import db
import argparse
import os

def get_caption(dir):
    session_file = os.path.join(dir,'session.db')
    if os.path.exists(session_file):
        db_url = 'sqlite:///{}'.format(session_file)
        db_file = db.DB(db_url)
        session = db_file.get_session()
        meta = session.query(db.Meta).first()
        return meta.url
    return ''


def parse_dir(dir, out_dir):
    print('Processing dir {}'.format(dir))
    for dirname, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith('.ts'):
                file_path = os.path.join(dirname, filename)
                caption = get_caption(dirname)
                out_file = file_path.replace('/','_')
                out_file = out_file.replace('\\', '_')
                out_file = out_file.replace(':', '_')
                out_file += '.jpg'
                out_file = os.path.join(out_dir, out_file)

                print('Processing file: {}, caption: {}, out file: {}'.format(file_path, caption, out_file))

                generate_thumb(file_path, out_file, caption)

        for subdir in dirnames:
            parse_dir(subdir, out_dir)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Video thumbnailer')
    parser.add_argument('dir', help='dir with videos')
    parser.add_argument('img_dir', help='dir for generated images')
    #parser.add_argument('-o', '--output', help='output folder name')
    #parser.add_argument('-s', '--session', help='output session name')

    args = parser.parse_args()

    parse_dir(args.dir, args.img_dir)
