MSG = "Last commit"


edit_paper:
	texmaker ./lg_env.tex ./references.bib &

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
	./bench/codes/*
	
	git commit -m "$(MSG)"

	
