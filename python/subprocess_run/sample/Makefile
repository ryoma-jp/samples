
# マクロ定義
CC           = gcc
CFLAGS       = -Wall
LDFLAGS      =
INCLUDES     = -I./
LIBS         =
TARGET       = sample
SRCS         = $(wildcard *.c)
OBJS         = $(SRCS:%.c=%.o)
DEPS         = $(SRCS:%.c=%.d)
RM           = rm

# 生成規則
.PHONY: all clean

all : $(TARGET)

-include $(DEPS)

$(TARGET) : $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(LIBS)

clean :
	$(RM) -f $(TARGET) $(OBJS) $(DEPS)

.c.o :
	$(CC) -c $(CFLAGS) $(INCLUDES) $<


