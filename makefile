#Commit mesage to update in git repo
MSG = "Last commit"
#Name of tex file
FILE_TEX  = lg_env
#Latex compiler
LATEX = pdflatex
#Viewer of pdf files
VIEWER = okular
#Latex editor
TEXEDIT = texmaker
#Current date
DATESTAMP=`date +'%Y-%m-%d'`


pdflatex:	$(FILE_TEX).tex  
		$(LATEX) $(FILE_TEX).tex 
		#Backup of pdf file (one per day)
		mkdir -p time-machine/${DATESTAMP}
		cp ${FILE_TEX}.pdf time-machine/${DATESTAMP}/${FILE_TEX}.pdf

clean:
		rm -f $(FILE_TEX).aux
		rm -f $(FILE_TEX).out
		rm -f $(FILE_TEX).bbl
		rm -f $(FILE_TEX).log

view: 
		$(VIEWER) $(FILE_TEX).pdf &

edit:
		$(TEXEDIT) $(FILE_TEX).tex &

update:
		git add \
		./figures/* 	\
		lg_env.tex	\
		lg_env.pdf	\
		makefile	\
		mn2e.bst	\
		mn2e.cls	\
		references.bib	\
		README		\
		macros.tex	\
		./bench/codes/*
	
		git commit -m "$(MSG)"

