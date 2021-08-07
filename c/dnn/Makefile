
# マクロ定義
CC           = gcc
#DEBUG        = -g
DEBUG        = 
CFLAGS       = -Wall
LDFLAGS      =
INCLUDES     = -I./
LIBS         =
TARGET       = dnn_inference
SRCS         = $(wildcard *.c)
OBJ_DIR      = ./build
OBJS         = $(SRCS:%.c=$(OBJ_DIR)/%.o)
DEPS         = $(SRCS:%.c=$(OBJ_DIR)/%.d)
RM           = rm
MKDIR        = mkdir

# 生成規則
.PHONY: all clean

all : $(TARGET)

$(TARGET) : $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(LIBS)

clean :
	$(RM) -f $(TARGET) $(OBJS) $(DEPS)

$(OBJ_DIR)/%.o : %.c
	$(MKDIR) -p $(OBJ_DIR)
	$(CC) $(DEBUG) -c $(CFLAGS) $(INCLUDES) -o $@ $<

-include $(DEPS)
