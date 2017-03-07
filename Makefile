DATADIR := data
RAWDIR := $(DATADIR)/raw
NORMDIR := $(DATADIR)/normalized
#OBJS := $(addprefix $(OBJDIR)/,foo.o bar.o baz.o)

compress: data.tar.gz

data.tar.gz: $(RAWDIR) $(NORMDIR)
	tar -zcvf data.tar.gz $(RAWDIR) $(NORMDIR)

decompress:
	tar -zxvf data.tar.gz

setup:
	mkdir figures
	mkdir figures/ura3-pq-replicate

parse:
	python data/parse/hsalinarum.py

database: .popmachine.db

.popmachine.db:
	# e. coli
	popmachine plate ecoli-eo499-propionicAcid-1 create data/normalized/lund/propionicAcid-ecoli/data.csv data/normalized/lund/propionicAcid-ecoli/meta.csv species=ecoli strain=eo499
	popmachine design setType pH float
	popmachine design setType propionicAcidmM float
	popmachine design setType rep int

	# h. salinarum
	popmachine plate hsal-gradientTest-1 create data/normalized/hsalinarum/gradientTest-1/data.csv data/normalized/hsalinarum/gradientTest-1/meta.csv species=hsal strain=ura3
	popmachine design setType mMPQ float
	popmachine design setType MNaCl float

clean:
	rm .popmachine.db
