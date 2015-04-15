OBJS := keys.o 
keys: $(OBJS)
	$(CXX) -o keys $(OBJS)
$(OBJS) : %.o : %.c
	$(CXX) -c $(CFLAGS) $< -o $@

