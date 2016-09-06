# htmlToRes
html text to res tags script

The script strips all text within a html file and creates res tags for the text. 
This can be useful when html files are included in your projects, to minimise the effort for translation purposes.

>Valid html is a prerequisite ie. correct opening and closing tags


`.bashrc alias`
```
alias htmlToRes='/home/jaminb/v2/temp/pkrasser/scripts/resTags/createResTags.py'
```
This script will convert all text within html tags (within a htm(l) file) to resTags. 
Pass in your html filenames as arguments ie.
```
htmlToRes filename1.html filename2.html 
``` 

For each file as argument a new version containing the resTags will be created. 
The new file names are the orignal filename +_resed.html. 
the above would create
```
filename1_resed.html filename2_resed.html
```

All resTags are saved in a new file named **AllResTags.xml**. 

Example can be found in the [example-createResTags](https://github.com/krasserp/resTags/tree/master/example-createResTags) folder where the script was run on the html file.
``` 
htmlToRes HTML_Tag__Create_a_Comment_Element_FocusVision_Knowledge_Base.html 
```

**Example usage:**
>The resTags can be added to your survey.xml.

>The refrenced html files in the html tags in the survey.xml can be replaced by the newly created yourfileName_resed.thml


