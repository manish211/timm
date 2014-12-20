


/^# / { 
    var=FILENAME; n=split (var,a,/\//); name=a[n]
    sub(".py","",name)
    $1=""; print "+ ["name"](" name ".md): " $0}
