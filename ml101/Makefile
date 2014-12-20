py=$(shell cd src; ls *.py)
md=$(subst src/,,$(subst .py,.md,$(py)))
url="https://github.com/ai-se/blob/master/timm/m101"

all: publish commit

typo:
	- git status
	- git commit -am "stuff"
	- git push origin master

commit:
	- git status
	- git commit -a
	- git push origin master

update:
	- git pull origin master

status:
	- git status

./%.md : src/%.py
	@bash etc/py2md $< $(url) > $@
	git add $@

README.md : etc/readme.txt $(md) etc/toc1.awk
	@cat $< > $@
	@echo "" >> $@
	@$(foreach f,$(py),\
		gawk -f etc/toc1.awk src/$f >> $@;)
	@echo "" >> $@
	git add $@

publish: $(md) README.md 
