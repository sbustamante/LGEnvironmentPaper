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


make_pdf:	$(FILE_TEX).tex  
		$(LATEX) $(FILE_TEX).tex 
		#Backup of pdf file (one per day)
		mkdir -p time-machine/${DATESTAMP}
		cp ${FILE_TEX}.pdf time-machine/${DATESTAMP}/${FILE_TEX}.pdf

clean:
		rm -f $(FILE_TEX).{aux,bbl,ps,pdf,div,blg,log}

view_pdf: 
		$(VIEWER) $(FILE_TEX).pdf &

edit_paper:
		$(TEXEDIT) $(FILE_TEX).tex &

git_update:
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

