BUILD_ALL += $(OUT_DIR)/example_detector_obstacle_rpi_xc112_r2b_xr112_r2b_a111_r2c

$(OUT_DIR)/example_detector_obstacle_rpi_xc112_r2b_xr112_r2b_a111_r2c : \
					$(OUT_OBJ_DIR)/example_detector_obstacle.o \
					libacc_detector_obstacle.a \
					libacconeer.a \
					libcustomer.a \
					$(OUT_OBJ_DIR)/acc_board_rpi_xc112_r2b_xr112_r2b.o
	@echo "    Linking $(notdir $@)"
	$(SUPPRESS)$(LINK.o) -Wl,--start-group $^ -Wl,--end-group $(LDLIBS) -o $@
