static void
make_blank (struct line *blank, int count)
 {
    int i;
    unsigned char *buffer;
    struct field *fields;
    blank->nfields = count;
    blank->buf.size = blank->buf.length = count + 1;
    blank->buf.buffer = (char*) xmalloc (blank->buf.size);
    buffer = (unsigned char *) blank->buf.buffer;
    blank->fields = fields = (struct field *) xmalloc (sizeof (struct field) * count);
    for (i = ; i < count; i++){
        // Code inside the loop
    }
 }
