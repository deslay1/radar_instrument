BUILD_ALL += $(OUT_DIR)/ref_app_rf_certification_test_rpi_xc112_r2b_xr112_r2b_a111_r2c

$(OUT_DIR)/ref_app_rf_certification_test_rpi_xc112_r2b_xr112_r2b_a111_r2c : \
					libacc_rf_certification_test.a \
					libacconeer.a \
					libcustomer.a \
					$(OUT_OBJ_DIR)/acc_board_rpi_xc112_r2b_xr112_r2b.o
	@echo "    Linking $(notdir $@)"
	$(SUPPRESS)$(LINK.o) -Wl,--start-group $^ -Wl,--end-group $(LDLIBS) -o $@
