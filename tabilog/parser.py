from api.models import Image

def gc(src):
    image = Image.objects.get(name=src)
    image.ref=0;
    image.save()

def parse(fin):

    s=fin.split("\n")
    res=""
    for line in s:

        if ("src=" in line) and ("class=\"lazyload\"" in line):
            seek_pre=line.find("src=")+5
            seek_las=line.find("\"",seek_pre)
            src=line[seek_pre:seek_las]
            gc(src)
            rep="src=\""+src+"\""
            new_src="src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==\" data-src=\""+src+"\""
            new_line=line.replace(rep,new_src)
            res+=new_line
        else:
            res+=line

    return res
