# Docker build failure log — 2026-02-04

## Command
docker build -t aws-meteo-backend .

## Output (trim only if huge; keep the error section intact)
"""
10.10 2026-02-04 06:17:58 (1.45 MB/s) - 'netcdf-c-4.9.2.tar.gz' saved [7142536/7142536]
10.10
11.52 configure: netCDF 4.9.2
11.54 checking build system type... x86_64-pc-linux-gnu
11.85 checking host system type... x86_64-pc-linux-gnu
11.85 checking target system type... x86_64-pc-linux-gnu
11.86 checking for gcc... gcc
12.01 checking whether the C compiler works... yes
12.19 checking for C compiler default output file name... a.out
12.20 checking for suffix of executables...
12.32 checking whether we are cross compiling... no
12.47 checking for suffix of object files... o
12.54 checking whether the compiler supports GNU C... yes
12.61 checking whether gcc accepts -g... yes
12.67 checking for gcc option to enable C11 features... none needed
12.78 checking whether gcc understands -c and -o together... yes
12.97 checking whether compiler supports -fno-strict-aliasing... yes
12.97 checking for a BSD-compatible install... /usr/bin/install -c
13.02 checking whether build environment is sane... yes
13.07 checking for a race-free mkdir -p... /usr/bin/mkdir -p
13.07 checking for gawk... gawk
13.08 checking whether make sets $(MAKE)... yes
13.15 checking whether make supports the include directive... yes (GNU style)
13.19 checking whether make supports nested variables... yes
13.22 checking dependency style of gcc... gcc3
13.37 checking whether to enable maintainer-specific portions of Makefiles... no
13.39 configure: checking supported formats
13.39 checking whether we should build with netcdf4 (alias for HDF5)... yes (deprecated; Please use with --disable-hdf5)
13.39 checking whether we should build with netcdf-4 (alias for HDF5)... yes
13.39 checking whether we should build with HDF5... yes
13.39 checking whether CDF5 support should be disabled... auto
13.39 checking whether reading of HDF4 SD files is to be enabled... no
13.39 checking whether parallel I/O for classic files is to be enabled... no
13.39 checking for curl_easy_setopt in -lcurl... no
13.51 checking whether DAP client(s) are to be built... no
13.51 configure: WARNING: curl required for dap access. DAP support disabled.
13.51 checking whether netcdf zarr storage format should be disabled... yes
13.51 checking whether netcdf-4 should be forcibly enabled... yes
13.51 configure: checking user options
13.51 checking whether a NCIO_MINBLOCKSIZE was specified... 256
13.51 checking for valgrind... no
13.51 checking if fsync support is enabled... no
13.51 checking if jna bug workaround is enabled... no
13.52 checking if unit tests should be enabled... yes
13.52 checking do we require hdf5 dynamic-loading support... yes
13.52 checking whether to fetch some sample HDF4 files from Unidata ftp site to test HDF4 reading (requires wget)... no
13.52 checking whether we should attempt to install netcdf-fortran (EXPERIMENTAL)... no
13.52 checking whether parallel IO tests should be run... no
13.52 checking whether a user specified program to run mpi programs... mpiexec
13.52 checking whether a default chunk size in bytes was specified... 4194304
13.52 checking whether a maximum per-variable cache size for HDF5 was specified... 67108864
13.52 checking whether a number of chunks for the default per-variable cache was specified... 10
13.52 checking whether a default file cache size for HDF5 was specified... 16777216
13.53 checking whether a default file cache maximum number of elements for HDF5 was specified... 4133
13.53 checking whether a default cache preemption for HDF5 was specified... 0.75
13.53 checking whether netCDF-4 logging is enabled... no
13.53 checking whether nc_set_log_level() function is included (will do nothing unless enable-logging is also used)... yes
13.60 checking whether CURLOPT_USERNAME is defined... no
13.67 checking whether CURLOPT_PASSWORD is defined... no
13.74 checking whether CURLOPT_KEYPASSWD is defined... no
13.81 checking whether CURLINFO_RESPONSE_CODE is defined... no
13.88 checking whether CURLOPT_BUFFERSIZE is defined... no
13.96 checking whether CURLOPT_TCP_KEEPALIVE is defined... no
13.96 checking whether libcurl is version 7.66 or later?... no
14.02 checking whether to search for and use external libxml2... yes
14.02 checking for xml2-config... xml2-config
14.03 checking for xmlReadMemory in -lxml2... yes
14.18 checking for library containing xmlReadMemory... -lxml2
14.50 checking whether to enable quantize functionality... yes
14.50 checking whether dap use of remotetest server should be enabled... no
14.50 checking whether dap use of remotetest server should be enabled... no
14.50 checking whether use of external servers should be enabled... no
14.50 configure: --disable-dap_remote_tests => --disable-external-server-tests
14.50 checking whether dap authorization testing should be enabled (default off)... no
14.50 configure: --disable-dap => --disable-dap-remote-tests --disable-auth-tests --disable-external-server-tests
14.50 checking which remote test server(s) to use... remotetest.unidata.ucar.edu
14.50 checking whether the time-consuming dap tests should be enabled (default off)... no
14.50 configure: --disable-dap-remote|external-server-tests => --disable_dap_long_tests
14.51 checking for blosc_init in -lblosc... no
14.63 checking for ZSTD_compress in -lzstd... no
14.75 checking whether libzstd library is available... no
14.75 checking for BZ2_bzCompress in -lbz2... no
14.87 checking whether libbz2 library is available... no
14.87 configure: Defaulting to internal libbz2
14.87 checking for SZ_BufftoBuffCompress in -lsz... no
14.99 checking whether libsz library is available... no
14.99 checking for library containing zip_open... no
15.50 checking whether libzip library is available... no
15.50 checking whether nczarr zip support is enabled... no
15.50 checking whether netcdf S3 support should be enabled... no
15.50 checking whether netcdf NCZarr S3 support should be enabled... no
15.50 checking whether AWS S3 SDK library is available... no
15.50 configure: WARNING: No S3 library available => S3 support disabled
15.50 checking whether netcdf zarr S3 testing should be enabled... no
15.50 checking whether a default file cache size for NCZarr was specified... 4194304
15.50 checking whether multi-filter support is enabled... yes
15.50 checking whether to enable strict null-byte header padding when reading (default off)... no
15.50 checking whether FFIO will be used... no
15.50 checking whether STDIO will be used... no
15.50 checking whether examples should be built... yes
15.50 checking whether v2 netCDF API should be built... yes
15.50 checking whether the ncgen/ncdump/nccopy should be built... yes
15.51 checking whether test should be built and run... yes
15.51 checking whether large file (> 2GB) tests should be run... no
15.51 checking whether benchmarks should be run... no
15.51 checking whether extreme numbers should be used in tests... yes
15.51 checking where to put large temp files if large file tests are run... .
15.51 checking Extra values for _NCProperties...
15.51 checking whether user-defined format 0 was specified...
15.51 checking whether a magic number for user-defined format 0 was specified...
15.51 checking whether user-defined format 1 was specified...
15.51 checking whether a magic number for user-defined format 1 was specified...
15.51 configure: finding C compiler
15.54 checking for gcc... (cached) gcc
15.67 checking whether the compiler supports GNU C... (cached) yes
15.67 checking whether gcc accepts -g... (cached) yes
15.67 checking for gcc option to enable C11 features... (cached) none needed
15.68 checking whether gcc understands -c and -o together... (cached) yes
15.68 checking for g++... g++
15.78 checking whether the compiler supports GNU C++... yes
15.94 checking whether g++ accepts -g... yes
16.02 checking for g++ option to enable C++11 features... none needed
16.35 checking dependency style of g++... gcc3
16.49 checking for an ANSI C-conforming const... yes
16.57 configure: setting up libtool
16.58 checking how to print strings... printf
16.59 checking for a sed that does not truncate output... /usr/bin/sed
16.62 checking for grep that handles long lines and -e... /usr/bin/grep
16.63 checking for egrep... /usr/bin/grep -E
16.64 checking for fgrep... /usr/bin/grep -F
16.65 checking for ld used by gcc... /usr/bin//ld
16.67 checking if the linker (/usr/bin//ld) is GNU ld... yes
16.68 checking for BSD- or MS-compatible name lister (nm)... /usr/bin//nm -B
16.69 checking the name lister (/usr/bin//nm -B) interface... BSD nm
16.78 checking whether ln -s works... yes
16.78 checking the maximum length of command line arguments... 1572864
16.82 checking how to convert x86_64-pc-linux-gnu file names to x86_64-pc-linux-gnu format... func_convert_file_noop
16.82 checking how to convert x86_64-pc-linux-gnu file names to toolchain format... func_convert_file_noop
16.82 checking for /usr/bin//ld option to reload object files... -r
16.82 checking for file... file
16.83 checking for objdump... objdump
16.83 checking how to recognize dependent libraries... pass_all
16.83 checking for dlltool... no
16.83 checking how to associate runtime and link libraries... printf %s\n
16.83 checking for ar... ar
16.83 checking for archiver @FILE support... @
16.93 checking for strip... strip
16.93 checking for ranlib... ranlib
16.93 checking command to parse /usr/bin//nm -B output from gcc object... ok
17.18 checking for sysroot... no
17.18 checking for a working dd... /usr/bin/dd
17.21 checking how to truncate binary pipes... /usr/bin/dd bs=4096 count=1
17.29 checking for mt... no
17.29 checking if : is a manifest tool... no
17.32 checking for dlfcn.h... yes
17.38 checking for objdir... .libs
17.62 checking if gcc supports -fno-rtti -fno-exceptions... no
17.70 checking for gcc option to produce PIC... -fPIC -DPIC
17.70 checking if gcc PIC flag -fPIC -DPIC works... yes
17.78 checking if gcc static flag -static works... no
17.85 checking if gcc supports -c -o file.o... yes
17.98 checking if gcc supports -c -o file.o... (cached) yes
17.98 checking whether the gcc linker (/usr/bin//ld -m elf_x86_64) supports shared libraries... yes
18.02 checking whether -lc should be explicitly linked in... no
18.13 checking dynamic linker characteristics... GNU/Linux ld.so
18.45 checking how to hardcode library paths into programs... immediate
18.45 checking whether stripping libraries is possible... yes
18.46 checking if libtool supports shared libraries... yes
18.46 checking whether to build shared libraries... yes
18.46 checking whether to build static libraries... yes
18.48 checking how to run the C++ preprocessor... g++ -E
19.09 checking for ld used by g++... /usr/bin//ld -m elf_x86_64
19.10 checking if the linker (/usr/bin//ld -m elf_x86_64) is GNU ld... yes
19.13 checking whether the g++ linker (/usr/bin//ld -m elf_x86_64) supports shared libraries... yes
19.50 checking for g++ option to produce PIC... -fPIC -DPIC
19.50 checking if g++ PIC flag -fPIC -DPIC works... yes
19.59 checking if g++ static flag -static works... no
19.66 checking if g++ supports -c -o file.o... yes
19.80 checking if g++ supports -c -o file.o... (cached) yes
19.80 checking whether the g++ linker (/usr/bin//ld -m elf_x86_64) supports shared libraries... yes
19.80 checking dynamic linker characteristics... (cached) GNU/Linux ld.so
19.83 checking how to hardcode library paths into programs... immediate
19.83 configure: finding other utilities
19.83 checking for m4... no
19.83 configure: error: Cannot find m4 utility. Install m4 and try again.
------
Dockerfile:36
--------------------
  35 |     WORKDIR /tmp
  36 | >>> RUN wget https://downloads.unidata.ucar.edu/netcdf-c/${NETCDF_VERSION}/netcdf-c-${NETCDF_VERSION}.tar.gz && \
  37 | >>>     tar -xzf netcdf-c-${NETCDF_VERSION}.tar.gz && \
  38 | >>>     cd netcdf-c-${NETCDF_VERSION} && \
  39 | >>>     CPPFLAGS="-I/usr/local/include" LDFLAGS="-L/usr/local/lib" ./configure --prefix=/usr/local --disable-dap && \
  40 | >>>     make -j$(nproc) && \
  41 | >>>     make install
  42 |
--------------------
ERROR: failed to build: failed to solve: process "/bin/sh -c wget https://downloads.unidata.ucar.edu/netcdf-c/${NETCDF_VERSION}/netcdf-c-${NETCDF_VERSION}.tar.gz &&     tar -xzf netcdf-c-${NETCDF_VERSION}.tar.gz &&     cd netcdf-c-${NETCDF_VERSION} &&     CPPFLAGS=\"-I/usr/local/include\" LDFLAGS=\"-L/usr/local/lib\" ./configure --prefix=/usr/local --disable-dap &&     make -j$(nproc) &&     make install" did not complete successfully: exit code: 1
(aws_backend) PS C:\Users\Asus\Documents\code\SbnAI\aws_meteo_backend> 
"""

## Notes
- Goal: AWS Lambda container image based on public.ecr.aws/lambda/python:3.12
- Multi-stage build: compile HDF5 + netcdf-c from source
- Must stay compatible with Amazon Linux 2023 runtime
