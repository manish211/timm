typo:
	- git status
	- git commit -am "fixing minor typo"
	- git push origin master

commit:
	- git status
	- git commit -a
	- git push origin master

update:
	- git pull origin master

status:
	- git status

F=genic

listing: etc/pdf/$F.pdf
	evince etc/pdf/$F.pdf &

etc/pdf/$F.pdf: $F.py
	mkdir -p etc/pdf
	a2ps --center-title="$F" -qr2gC --columns 3 --font-size 7  --prologue=color  -o ~/tmp/listing.ps $F.py
	ps2pdf  ~/tmp/listing.ps	
	mv listing.pdf etc/pdf/$F.pdf

demo:
	python genic.py 
