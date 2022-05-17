# -*-coding:utf-8-*-
import os
import random
import shutil

#做复合物结构图或氢键图
def complex2pdb2bmp(j):
    with open("complex2pdb2bmp.txt", "w") as f:
        if j == 1:
            f.write("complex2\nrenderall\nexit")
        if j == 2:
            f.write("hbond\nrenderall\nexit")

    pdblist = getfiles("pdb")
    for i in pdblist:
        os.system("C:\\vmd\\vmd.exe -dispdev text -e complex2pdb2bmp.txt " + i)
    os.remove("complex2pdb2bmp.txt")

#给pdb加box，输出分子尺寸信息。
def pdb2size():
    with open("pdb2size.txt","w") as f:
        f.write("100\n 21\nsize\n 2\n 0\n q\n 0\n q")
    pdblist = getfiles("pdb")
    for i in pdblist:
        name = os.path.splitext(i)[0]
        os.system("Multiwfn.exe " + i + " < pdb2size.txt > " + name + "-size.txt")
        shutil.move("new.pdb", name + "-size.pdb")
    os.remove("pdb2size.txt")

    with open("size2bmp.txt","w") as f:
        f.write("showbox\n complex2\n renderbox\n exit")
    sizelist = getfiles("-size.pdb")
    for i in sizelist:
        os.system("C:\\vmd\\vmd.exe -dispdev text -e size2bmp.txt " + i)
    os.remove("size2bmp.txt")

#将fchk文件转化为MEP所需的cub文件。
def fchk2elecub():
    with open("fchk2elecub.txt", "w") as f:
        f.write("5\n 1\n 3\n 2\n 0\n 5\n 12\n 1\n 2\n 0\n q")  #第3，8个数字控制电子密度，静电势的格点数

    fchklist = getfiles("fchk")
    for i in fchklist:
        os.system("Multiwfn.exe " + i + " < fchk2elecub.txt")
        name = os.path.splitext(i)[0]
        shutil.move("density.cub", name + "-density.cub")
        shutil.move("totesp.cub", name + "-totesp.cub")
    os.remove("fchk2elecub.txt")

#使用fchk2elecub输出的cub文件做MEP图
def elecub2bmp(j):
    k1 = "-0.03"
    k2 = "0.03"
    if j != 0:
        k1 = input("""输入填色最小值，直接回车为默认值-0.03：
    (Input min of colorscale, or the min will be default -0.03 by directly hit enter)\n""") or "-0.03"
        k2 = input("""输入填色最大值，直接回车为默认值0.04：
    (Input max of colorscale, or the max will be default 0.03 by directly hit enter)\n""") or "0.03"
    if j == 1:
        k3 = "renderone"
    else:
        k3 = "renderall"
    cublist = getfiles("density.cub")
    for i in cublist:
        name = i[0:-12]
        with open("elecub2bmp.txt", "w") as f1:
            f1.write("mol addfile " + name + """-totesp.cub\ndrawmep
mol scaleminmax top 1 """ + k1 + " " + k2 + "\n" + k3 + "\nexit")
        os.system("C:\\vmd\\vmd.exe -dispdev text -e elecub2bmp.txt " + name + "-density.cub")
        os.remove("elecub2bmp.txt")

def name2res0serial(j):
    with open("name2res0serial.txt", "w") as f:
        f.write("outputres0serial\nexit")
    os.system("C:\\vmd\\vmd.exe -dispdev text -e name2res0serial.txt " + j + ".pdb")
    os.remove("name2res0serial.txt")

#将fchk文件转化为IGMH所需的cub文件
def fchk2igmhcub(j):
    fchklist = getfiles("fchk")
    for i in fchklist:
        name = os.path.splitext(i)[0]
        if j == 0:
            k = input("""\n1.使用Multiwfn转化的pdb判断片段原子号。
    (Get atom numbers using pdb files coverted by Multiwfn.)
2.使用Openbabel转化的pdb判断片段原子号。
    (Get atom numbers using pdb files coverted by Openbabel.)\n""")
            if k == 1:
                file2pdb(i)
            else:
                os.system("obabel " + i + " -opdb -O " + name + ".pdb")
            name2res0serial(name)
            os.remove(name + ".pdb")
            with open("serial.txt","r") as f1:
                serial = f1.read().replace(" ",",")
        else:
            serial = j + "\n"
        with open("fchk2igmhcub.txt", "w") as f2:
            f2.write("20\n 11\n 2\n " + serial + "c\n -10\n 0\n 3\n 3\n 0\n 0\n q")  # 倒数第5个数字控制计算级别
        os.system("Multiwfn.exe " + i + " < fchk2igmhcub.txt")
        shutil.move("sl2r.cub", name + "-sl2r.cub")
        shutil.move("dg_inter.cub", name + "-dg_inter.cub")
    os.remove("fchk2igmhcub.txt")
    os.remove("dg_intra.cub")
    os.remove("dg.cub")
    os.remove("serial.txt")

#使用fchk2igmhcub输出的cub文件做IGMH图
def igmhcub2bmp(j):
    k1 = "0.005"
    k2 = "-0.04"
    k3 = "0.04"
    if j != 0:
        k1 = input("""\n输入等值面数值，直接回车为默认值0.005：
(Input value of isosurface, or the value will be default 0.005 by directly hit enter)\n""") or "0.005"
        k2 = input("""输入填色最小值，直接回车为默认值-0.04：
(Input min of colorscale, or the min will be default -0.04 by directly hit enter)\n""") or "-0.04"
        k3 = input("""输入填色最大值，直接回车为默认值0.04：
(Input max of colorscale, or the max will be default 0.04 by directly hit enter)\n""") or "0.04"
    if j == 1:
        k4 = "renderone"
    else:
        k4 = "renderall"
    cublist = getfiles("sl2r.cub")
    for i in cublist:
        name = i[0:-9]
        with open("igmhcub2bmp.txt", "w") as f1:
            f1.write("mol addfile " + name + """-dg_inter.cub\ndrawigm
mol modstyle 2 top Isosurface """ + k1 + " 1 0 0 1 1\n mol scaleminmax top 2 " \
+ k2 + " " + k3 + "\n" + k4 + "\nexit")
        os.system("C:\\vmd\\vmd.exe -dispdev text -e igmhcub2bmp.txt " + name + "-sl2r.cub")
        os.remove("igmhcub2bmp.txt")

#获得文件末尾为suf的文件名列表
def getfiles(suf):
    directory = os.getcwd()
    filelist = []
    for i in os.listdir(directory):
        path = os.path.join(directory, i)
        if os.path.isfile(path):
            if path.endswith(suf):
                filelist.append(i)
    return filelist

#给openbabel转化suf文件输出的gjf文件加计算资源、默认关键词信息
def normobgjf(suf):
    suflist = getfiles(suf)
    for file in suflist:
        name = os.path.splitext(file)[0]
        with open(name + ".gjf","r+") as f:
            old = f.readlines()[2:]
            f.seek(0)
            f.write("%nprocshared=24\n%mem=45gb\n%chk=" + name + \
".chk\n#p opt freq b3lyp/6-31G(d) em=gd3 scrf=smd\n")
            for line in old:
                f.write(line)


def alter(file, old_str, new_str):
    file_data = ""
    with open(file, "r") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str, new_str)
            file_data += line
    with open(file, "w") as f:
        f.write(file_data)

#使用Multiwfn将任意文件转化为pdb文件
def file2pdb(j):
    with open("file2pdb.txt", "w") as f:
        f.write("100\n 2\n 1\n\n 0\n q")

    filelist = getfiles(j)
    for i in filelist:
        os.system("Multiwfn.exe " + i + " < file2pdb.txt")
        name = os.path.splitext(i)[0]
    os.remove("file2pdb.txt")

#使用gview打开结尾为suf的文件
def openfile(suf):
    filelist = getfiles(suf)
    for i in filelist:
        os.system("gview.exe " + i)


a = eval(input("""仔宝宝想做什么任务呢？(What do you want to do, baby zai?)
1.结构图。(Pictures of structures.)
2.分子表面静电势（MEP）图。(Molecular Electrostatic Potential graphs.)
3.IGMH图。(IGMH pictures.)
4.文件格式转换及其它小工具。(Converting file formats and other small tools.)
100.打豚鼠。(Hit porcellus.)\n"""))
if a == 1:
    b = eval(input("""\n1.主客体复合物结构图。
    (Drawing graphs for all host-guest complex structures.)
2.做分子尺寸图。
    (Showing the molecular size.)
3.做氢键图。
    (Showing the Hbonds.)\n"""))
    if b == 1:
        complex2pdb2bmp(1)
    if b == 2:
        pdb2size()
    if b == 3:
        complex2pdb2bmp(2)

if a == 2:
    b = eval(input("""\n1.直接一步做MEP图。默认设定转化所有fchk为MEP图。
    (Converting all fchk files to MEP pictures using default setting.)
2.分步做MEP图。第一步：转化所有fchk文件为cub文件。
    (Drawing MEP pictures step by step. Step 1: converting all fchk files to cub files.)
3.分步做MEP图。第二步：转化cub文件为一张MEP图，并调整作图参数。
    (Drawing MEP pictures step by step. \
Step 2: converting cub file to one MEP picture and changing the setting of MEP pictures.)
4.分步做MEP图。第三步：按照上一步调整好的作图参数，转化所有cub文件为MEP图。
    (Drawing MEP pictures step by step. \
Step 3: converting all cub files to MEP pictures according to the setting in the last step.)\n"""))
    if b == 1:
        fchk2elecub()
        elecub2bmp(0)
    if b == 2:
        fchk2elecub()
    if b == 3:
        elecub2bmp(1)
    if b == 4:
        elecub2bmp(2)
    else:
        print("输入错误。\nWrong input.")

if a == 3:
    b = eval(input("""\n1.直接一步做IGMH图。默认设定转化所有fchk为IGMH图。
    (Converting all fchk files to IGMH pictures using default setting.)
2.分步做IGMH图。第一步：转化所有fchk文件为cub文件。
    (Drawing IGMH pictures step by step. Step 1: converting all fchk files to cub files.)
3.分步做IGMH图。第二步：转化cub文件为一张IGMH图，并调整作图参数。
    (Drawing IGMH pictures step by step. \
Step 2: converting cub file to one IGMH picture and changing the setting of IGMH pictures.)
4.分步做IGMH图。第三步：按照上一步调整好的作图参数，转化所有cub文件为IGMH图。
    (Drawing IGMH pictures step by step. \
Step 3: converting all cub files to IGMH pictures according to the setting in the last step.)\n"""))
    if b == 1:
        nums = input("""请输入一个片段的原子序号范围。例如1-217,256,278-290。直接回车使用软件默认判断
(Please input the range of atom numbers of a fragment. e.g. 1-217,256,278-290):\n""") or 0
        fchk2igmhcub(nums)
        igmhcub2bmp(0)
    if b == 2:
        nums = input("""请输入一个片段的原子序号范围。例如1-217,256,278-290。直接回车使用软件默认判断
(Please input the range of atom numbers of a fragment. e.g. 1-217,256,278-290):\n""") or 0
        fchk2igmhcub(nums)
    if b == 3:
        igmhcub2bmp(1)
    if b == 4:
        igmhcub2bmp(2)
    else:
        print("输入错误。\nWrong input.")
if a == 4:
    b = eval(input("""\n----------查看文件部分----------
1. 用Gaussview打开所有指定文件。
    (Open all files using Gaussview.)\n
----------转为pdb文件部分----------
2.将所有cdx文件转为3D版的pdb，在pH7.4的条件下加氢，并用MMFF94力场优化结构。
    (Converting all the cdx files into pdb files, adding hydrogen at pH 7.4, \
 and optimizing the structure by MMFF94 force field.)
3.使用Multiwfn将所有指定文件类型转为pdb。
    (Converting all files into pdb files using Multiwfn.)
4.使用Openbabel将所有指定文件类型转为pdb。
    (Converting all files into pdb files using Openbabel.)\n
----------转为gjf文件部分----------
5.使用Openbabel将所有指定文件类型转为gjf。
    (Converting all files into gjf files using Openbabel.)\n
"""))
    if b == 1:
        openfile(input("""请输入想打开文件的后缀名。如fchk
(Input the suffix of the files needing to open. e.g. fchk)\n"""))
    if b == 2:
        os.system("obabel *.cdx -opdb -m --gen3d -p --minimize --ff MMFF94")
    if b == 3:
        file2pdb(input("""请输入想转换文件的后缀名。如fchk
(Input the suffix of the files needing to convert. e.g. fchk)\n"""))
    if b == 4:
        suf = input("""请输入想转换文件的后缀名。如fchk
(Input the suffix of the files needing to convert. e.g. fchk)\n""")
        os.system("obabel *." + suf + " -opdb -m")
    if b == 5:
        suf = input("""请输入想转换文件的后缀名。如fchk
(Input the suffix of the files needing to convert. e.g. fchk)\n""")
        os.system("obabel *." + suf + " -ogjf -m")
        normobgjf(suf)
if a == 100:
    ls = ["6275275109475431293ffe1e.gif","6275288a0947543129469e46.gif",\
          "627527a4094754312941b551.gif","62752f9609475431296cc27a.gif",\
          "62752f9609475431296cc281.gif","62752f9609475431296cc294.gif",\
          "62752f9609475431296cc2ac.gif","62752f9609475431296cc2e7.gif",\
          "627531ee094754312975acc7.gif","6275321d0947543129765917.gif",\
          "6275330f094754312979a6af.gif","6275330f094754312979a6b7.gif",\
          "6275330f094754312979a6be.gif","6275330f094754312979a719.gif",\
          "6275330f094754312979a725.gif"]
    b = random.randint(0,len(ls)-1)
    os.system("start https://pic.imgdb.cn/item/" + ls[b])
else:
    print("输入错误。\nWrong input.")
