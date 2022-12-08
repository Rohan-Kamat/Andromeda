import click
import sys
import os

sys.path.append('C:\\Users\\ROHAN\\Documents\\Andromeda')

@click.command()
@click.argument("content_path")
def parse(content_path):
    if not(os.path.exists(content_path)):
        click.echo("Invalid Path: No such file found")
        return 


    from src.htmlParser import htmlParser
    f = open(content_path,'r')
    content = f.read()
    parser = htmlParser(content)

    links = parser.getLinks()
    words = parser.getWords()

    link_file = open("C:\\Users\\ROHAN\\Documents\\Andromeda\\assets\\links.txt",'w')
    word_file = open("C:\\Users\\ROHAN\\Documents\\Andromeda\\assets\\words.txt",'w')

    for link in links:
        link_file.write(link + '\n')
    
    for word in words:
        word_file.write(word + ' ')
    







