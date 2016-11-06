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
