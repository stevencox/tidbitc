import argparse
import os
import requests
import yaml

class TidbitCompiler:
    """ Generate a tidbit. """
    def __init__(self, conf):
        self.conf = conf
    
    def create_site(self, name, theme, title):
        """ Create the site. """
        os.system (f"hugo new site {name}")
        posts = os.path.join (name, "posts")
        if not os.path.exists (posts):
            os.makedirs (posts)
        os.chdir (f"{name}")

        add_theme_command = f"git clone https://github.com/budparr/gohugo-theme-{theme}.git themes/{theme} "
        '''
        print (f"theem repo ----------- {theme_repo}")
        if theme_repo is not None:
            add_theme_command = f"git clone {theme_repo} themes/{theme}"
        '''
        print (add_theme_command)
        os.system (add_theme_command)

        file_name = "config.toml"
        config_text = None
        with open (file_name, "r") as stream:
            config_text = stream.read ()

        config_text = config_text.replace ("My New Hugo Site", title)
        config_text = f"""{config_text}
theme = "{theme}" 
[params]
  recent_posts_number = 10
"""
        with open (file_name, "w") as stream:
            stream.write (config_text)
          
    def make_post(self, name=None, text=None, issue_id=None):
        """ Generate the post. """
        post_name = os.path.join ("posts", f"{name}.md")
        file_name = os.path.join ("content", post_name)
        body = ""
        if issue_id is not None:
            url = f"https://api.github.com/repos/ncats/translator-workflows/issues/{issue_id}"
            response = requests.get (url).json ()
            body = response['body']
        if text is not None:
            body = f"{body}\n{text}"

        if body is not None:
            make_post = f"hugo new '{post_name}'"
            print (f"--- {make_post}")
            os.system (make_post)
            with open (post_name, "a") as stream:
                stream.write (body)
                
    def run (self):
        self.create_site (**self.conf['header'])
        for post in self.conf['body']: #['posts']:
            print(f"making post: {post}")
            self.make_post (**post)
        os.system ("cp -r ../static .")
        os.system ("mv posts content") # not clear why this is needed.
        
def run ():            
    arg_parser = argparse.ArgumentParser(
        description='TidbitC - A Translator TIDBIT compiler.',
        formatter_class=lambda prog: argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=60))
    arg_parser.add_argument('-c', '--conf', help="Config file.", default="tidbitc.yaml")
    args = arg_parser.parse_args ()
    with open (args.conf, "r") as stream:
        conf = yaml.load (stream)
        compiler = TidbitCompiler (conf)
        compiler.run ()
    
if __name__ == '__main__':
    run ()
