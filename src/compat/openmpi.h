/* $Id$ */

#ifndef PyMPI_COMPAT_OPENMPI_H
#define PyMPI_COMPAT_OPENMPI_H

#if defined(OPEN_MPI) 

/* ---------------------------------------------------------------- */

#if !defined(OPEN_MPI_DLOPEN_LIBMPI)
#define OPEN_MPI_DLOPEN_LIBMPI 1
#endif

#if OPEN_MPI_DLOPEN_LIBMPI

#if !defined(LTDL_H)

#if defined(__cplusplus)
#define LT_BEGIN_C_DECLS extern "C" {
#define LT_END_C_DECLS }
#else /* !__cplusplus */
#define LT_BEGIN_C_DECLS
#define LT_END_C_DECLS
#endif

#if defined(OMPI_DECLSPEC)
#define LT_SCOPE OMPI_DECLSPEC
#else /* !OMPI_DECLSPEC */
#define LT_SCOPE extern
#endif

LT_BEGIN_C_DECLS

typedef	void *lt_dlhandle;
typedef void *lt_dladvise;
LT_SCOPE int lt_dlinit (void);
LT_SCOPE int lt_dlexit (void);
LT_SCOPE int lt_dladvise_init    (lt_dladvise *advise);
LT_SCOPE int lt_dladvise_destroy (lt_dladvise *advise);
LT_SCOPE int lt_dladvise_ext     (lt_dladvise *advise);
LT_SCOPE int lt_dladvise_global  (lt_dladvise *advise);
LT_SCOPE lt_dlhandle lt_dlopenadvise (const char *filename, lt_dladvise advise);
LT_SCOPE int lt_dlclose (lt_dlhandle handle);

LT_END_C_DECLS

#endif /* !LTDL_H */

static int         PyMPI_OPENMPI_ltdlup = 0;
static lt_dlhandle PyMPI_OPENMPI_handle = 0; 

static void dlopen_mpi_lib(void)
{
  const char *filename = "libmpi";
  int         ltdlup = PyMPI_OPENMPI_ltdlup;
  lt_dlhandle handle = PyMPI_OPENMPI_handle;
  if (ltdlup == 0) {
    ltdlup = (lt_dlinit() == 0);
  }
  if (ltdlup != 0 && handle == 0) {
    lt_dladvise	advise;
    if (!lt_dladvise_init(&advise) &&
	!lt_dladvise_ext(&advise)  &&
	!lt_dladvise_global(&advise))
      handle = lt_dlopenadvise(filename, advise);
    lt_dladvise_destroy (&advise);
  }
  PyMPI_OPENMPI_ltdlup = ltdlup;
  PyMPI_OPENMPI_handle = handle;
}

static void dlclose_mpi_lib(void)
{
  int         ltdlup = PyMPI_OPENMPI_ltdlup;
  lt_dlhandle handle = PyMPI_OPENMPI_handle;
  if (ltdlup != 0 && handle != 0) {
    lt_dlclose(handle);
    handle = 0;
  }
  if (ltdlup != 0) {
    lt_dlexit();
    ltdlup = 0;
  }
  PyMPI_OPENMPI_ltdlup = ltdlup;
  PyMPI_OPENMPI_handle = handle;
}

static int PyMPI_OPENMPI_MPI_Init(int *argc, char ***argv)
{
  int ierr = MPI_SUCCESS;
  dlopen_mpi_lib();
  ierr = MPI_Init(argc, argv);
  return ierr;
}
#undef  MPI_Init
#define MPI_Init PyMPI_OPENMPI_MPI_Init

static int PyMPI_OPENMPI_MPI_Init_thread(int *argc, char ***argv,
					 int required, int *provided)
{
  int ierr = MPI_SUCCESS;
  dlopen_mpi_lib();
  ierr = MPI_Init_thread(argc, argv, required, provided);
  return ierr;
}
#undef  MPI_Init_thread
#define MPI_Init_thread PyMPI_OPENMPI_MPI_Init_thread

static int PyMPI_OPENMPI_MPI_Finalize(void)
{
  int ierr = MPI_SUCCESS;
  ierr = MPI_Finalize();
  dlclose_mpi_lib();
  return ierr;
}
#undef  MPI_Finalize
#define MPI_Finalize PyMPI_OPENMPI_MPI_Finalize

#endif /* !OPEN_MPI_DLOPEN_LIBMPI */

/* ---------------------------------------------------------------- */

/*
 * Open MPI 1.1 generates an error when MPI_File_get_errhandler() is
 * called with the MPI_FILE_NULL handle.  The code below try to fix
 * this bug by intercepting the calls to the functions setting and
 * getting the error handlers for files.
 *
 */

#if !defined(OMPI_MAJOR_VERSION) || OMPI_MAJOR_VERSION==1
#if !defined(OMPI_MINOR_VERSION) || OMPI_MINOR_VERSION<=1

static MPI_Errhandler PyMPI_OPENMPI_FILE_NULL_ERRHANDLER = (MPI_Errhandler)0;

static int PyMPI_OPENMPI_File_get_errhandler(MPI_File file, MPI_Errhandler *errhandler)
{
  if (file == MPI_FILE_NULL) {
    if (PyMPI_OPENMPI_FILE_NULL_ERRHANDLER == (MPI_Errhandler)0) {
      PyMPI_OPENMPI_FILE_NULL_ERRHANDLER = MPI_ERRORS_RETURN;
    }
    *errhandler = PyMPI_OPENMPI_FILE_NULL_ERRHANDLER;
    return MPI_SUCCESS;
  }
  return MPI_File_get_errhandler(file, errhandler);
}
#undef  MPI_File_get_errhandler
#define MPI_File_get_errhandler PyMPI_OPENMPI_File_get_errhandler

static int PyMPI_OPENMPI_File_set_errhandler(MPI_File file, MPI_Errhandler errhandler)
{
  int ierr = MPI_File_set_errhandler(file, errhandler);
  if (ierr != MPI_SUCCESS) return ierr;
  if (file == MPI_FILE_NULL) {
    PyMPI_OPENMPI_FILE_NULL_ERRHANDLER = errhandler;
  }
  return ierr;
}
#undef  MPI_File_set_errhandler
#define MPI_File_set_errhandler PyMPI_OPENMPI_File_set_errhandler

#endif /* !OMPI_MINOR_VERSION<=1 */
#endif /* !OMPI_MAJOR_VERSION==1 */

/* ---------------------------------------------------------------- */

#endif /* !OPEN_MPI */

#endif /* !PyMPI_COMPAT_OPENMPI_H */
