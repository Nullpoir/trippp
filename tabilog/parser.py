from api.models import Image


def apply_del_flag(src):
    image = Image.objects.get(name=src)
    image.ref=1;
    image.save()

def apply_save_flag(src):
    image = Image.objects.get(name=src)
    image.ref=0;
    image.save()

def alldel(fin):
    s=fin.split("\n")
    res=""

    for line in s:
        if ("src=" in line) and ("img" in line) and not ("lazyload" in line):
            seek_pre=line.find("src=")+5
            seek_las=line.find("\"",seek_pre)
            src=line[seek_pre:seek_las]
            apply_del_flag(src)

def allsave(fin):
    s=fin.split("\n")
    res=""

    for line in s:
        if ("src=" in line) and ("img" in line) and not ("lazyload" in line):
            seek_pre=line.find("src=")+5
            seek_las=line.find("\"",seek_pre)
            src=line[seek_pre:seek_las]
            apply_save_flag(src)

def parse(fin):

    s=fin.split("\n")
    res=""
    for line in s:

        if ("src=" in line) and ("img" in line) and not ("lazyload" in line):
            seek_pre=line.find("src=")+5
            seek_las=line.find("\"",seek_pre)
            src=line[seek_pre:seek_las]
            apply_save_flag(src)
            rep="src=\""+src+"\""
            new_src="class=\"lazyload\" src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==\" data-src=\""+src+"\""
            new_line=line.replace(rep,new_src)
            res+=new_line
        else:
            res+=line

    return res
