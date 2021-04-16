# Exporting MICs from the VITEK database
## Database acquition
First you will need to obtain database files from the computer used to run the VITEK software. On this computer, they are located at:
```bash
D:\VITEK 2 compact\database\postgresql\data_801\
```
Transfer the `data_801/` directory to M3 using a USB or private cloud storage (e.g. Google Drive).


## Software provisioning
On M3, clone this repo and change directory:
```bash
git clone https://github.com/scwatts/vitek_export.git && cd vitek_export/
```

In order to open the VITEK database we must use the same version of postgres (and same compilation options) that is used in
the VITEK software. There is no pre-compiled postgres release that works in this context and consequently we need to manually
compile the software ourselves.

Download the source and extract into its own directory:
```bash
mkdir -p software/
wget -P software/ https://ftp.postgresql.org/pub/source/v9.2.0/postgresql-9.2.0.tar.gz
tar -zxvf software/postgresql-9.2.0.tar.gz -C software/ && cd software/postgresql-9.2.0/
```

Next, configuration the software for compilation:
```bash
./configure --prefix=$(pwd -P)/../ --disable-float8-byval
```

Compile and install, then return to tld:
```bash
make -j4 && make install
cd ../../
```

## Prepare database files
Move the database directory `data_801/` into the repo directory. Ensure that this directory has the correct permissions as
required by the postgres server software:
```bash
chmod 700 data_801/
```

Allow the postgres client software to connect to the database without a password:
```bash
sed -i '/^host / { s/md5\r/trust/ }' data_801/pg_hba.conf
```


## Export MICs
Now that the postgres software and VITEK database files are ready, we can export the MICs. To do this we first start the
postgres server for the database files:
```bash
./software/bin/postgres -D data_801/ -h localhost -p 50808
```

Finally, we can create an output directory and execute the export:
```bash
mkdir -p output/
./software/bin/psql -U postgres -h localhost -p 50808 -f scripts/export_mics.sql | tail -n+2 > output/vitek_mics_export.csv
```

Optionally this data can be cast to a wide format, which can be useful for importing this data into the lab database. To run this on M3 you will need to have loaded the R environment and installed the `reshape2` package.
```bash
./scripts/cast_data.R output/vitek_mics_export.csv output/vitek_mics_export_wide.csv
```
