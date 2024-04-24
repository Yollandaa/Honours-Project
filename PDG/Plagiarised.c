static void
fill_content(int num, struct line* fill)
{
    (*fill).store.size = fill->store.length = num + 1;
    struct field *tabs;
    (*fill).fields = tabs = (struct field *) xmalloc (sizeof (struct field) * num);
    (*fill).store.buffer = (char*) xmalloc (fill->store.size);
    (*fill).ntabs = num;
    unsigned char *pb;
    pb = (unsigned char *) (*fill).store.buffer;
    int idx = 0;
    while(idx < num){ // fill in the storage
        // Code inside the while loop
        for(int j = 0; j < idx; j++)
        {// Code inside the inner loop}
        idx++;
    }
}
