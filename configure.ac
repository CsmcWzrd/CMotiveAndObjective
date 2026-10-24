AC_INIT([CMotiveAndObjective],[1.0.0])
AC_CONFIG_SRCDIR([src/CMotiveAndObjective.CMOT])
AM_INIT_AUTOMAKE([foreign subdir-objects])
AC_PROG_CC
AC_PROG_INSTALL
AC_ARG_VAR([CMOTIVE_ROOT],[absolute CMotive root])
AC_ARG_VAR([CMOTIVE],[CMotive compiler executable])
AS_IF([test -z "$CMOTIVE_ROOT"],[AC_MSG_ERROR([set CMOTIVE_ROOT to absolute compiler source root])])
AS_IF([test -z "$CMOTIVE"],[CMOTIVE="$CMOTIVE_ROOT/build/bin/cmotive"])
AS_IF([test ! -x "$CMOTIVE"],[AC_MSG_ERROR([CMotive compiler is not executable])])
AS_IF([test ! -f "$CMOTIVE_ROOT/lib/Sys/runtime.c"],[AC_MSG_ERROR([CMOTIVE_ROOT lacks compiler runtime])])
AC_PATH_PROG([PYTHON],[python3])
AS_IF([test -z "$PYTHON"],[AC_MSG_ERROR([python3 required for behavioral tests])])
AC_CANONICAL_HOST
AS_CASE([$host_os],[darwin*],[CMO_EXT=dylib; CMO_SHARED='-dynamiclib -Wl,-install_name,@rpath/libCMotiveAndObjective-1.0.0.dylib'; CMO_EXPORTS='-Wl,-exported_symbols_list,$(srcdir)/build-support/exports.macos'],[linux*],[CMO_HARDEN="-fstack-protector-strong -Wl,--no-undefined,-z,relro,-z,now,-z,noexecstack"; CMO_EXT=so; CMO_SHARED='-shared -Wl,-soname,libCMotiveAndObjective-1.0.0.so'; CMO_EXPORTS='-Wl,--version-script=$(srcdir)/build-support/exports.map'],[AC_MSG_ERROR([use CMake for this platform])])
AC_SUBST([CMO_HARDEN])
AC_SUBST([CMO_EXT])
AC_SUBST([CMO_SHARED])
AC_SUBST([CMO_EXPORTS])
AC_CONFIG_FILES([Makefile])
AC_OUTPUT
