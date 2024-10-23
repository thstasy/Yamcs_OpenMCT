#include <stdio.h>
#include <stdint.h>

#define SLOT_SIZE 4000

typedef struct {
    uint16_t slot_cnt;
    uint16_t daq_no;
    int32_t tv_sec;
    int32_t tv_nsec;
    uint8_t data[SLOT_SIZE];
} tlm_t;

int main(int argc, char *argv[])
{
    FILE *fptr = fopen(argv[1], "rb");
    FILE *optr = fopen("accel_out.csv", "w");
    tlm_t t;

    // Header
    fprintf(optr, "daq_no, slot_cnt, slot_sec, slot_nsec, check, ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7\n");

    // Data
    while(fread(&t, sizeof(tlm_t), 1, fptr)) {
        uint16_t *dptr = &(t.data[0]);
        for(int i = 0;i < 250;++i) {
            fprintf(optr, "%u, %u, %d, %d, %d", t.daq_no, t.slot_cnt, t.tv_sec, t.tv_nsec, *dptr >> 12);
            for(int j = 0;j < 8;++j) {
                fprintf(optr, ", %d", *dptr & 0xFFF);
                dptr++;
            }
            fputs("\n", optr);
        }
    }

    fclose(fptr);
    fclose(optr);

    return 0;
}
