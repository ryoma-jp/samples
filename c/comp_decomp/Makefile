
# マクロ定義
CC           = gcc
CFLAGS       = -Wall
LDFLAGS      =
INCLUDES     = -I./
LIBS         =
TARGET       = comp_decomp
SRCS         = $(wildcard *.c)
OBJ_DIR      = ./build
OBJS         = $(SRCS:%.c=$(OBJ_DIR)/%.o)
DEPS         = $(SRCS:%.c=$(OBJ_DIR)/%.d)
RM           = rm

# 生成規則
.PHONY: all clean

all : $(TARGET)

$(TARGET) : $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(LIBS)

clean :
	$(RM) -f $(TARGET) $(OBJS) $(DEPS)

$(OBJ_DIR)/%.o : %.c
	$(CC) -c $(CFLAGS) $(INCLUDES) -o $@ $<

-include $(DEPS)
