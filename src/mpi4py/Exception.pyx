cdef class Exception(RuntimeError):

    """
    Exception
    """

    def __cinit__(self, int ierr=0):
        if ierr < MPI_SUCCESS:      ierr = MPI_ERR_UNKNOWN
        if ierr > MPI_ERR_LASTCODE: ierr = MPI_ERR_UNKNOWN
        self.ob_mpi = ierr
        RuntimeError.__init__(self, ierr)

    def __richcmp__(Exception self, int error, int op):
        cdef int ierr  = self.ob_mpi
        if op == 0: return ierr <  error
        if op == 1: return ierr <= error
        if op == 2: return ierr == error
        if op == 3: return ierr != error
        if op == 4: return ierr >  error
        if op == 5: return ierr >= error

    def __nonzero__(self):
        return self.ob_mpi != MPI_SUCCESS

    def __bool__(self):
        return self.ob_mpi != MPI_SUCCESS

    def __int__(self):
        if not _mpi_active(): return self.ob_mpi
        return self.Get_error_code()

    def __str__(self):
        if not _mpi_active(): return "error code: %d" % self.ob_mpi
        return self.Get_error_string()

    def Get_error_code(self):
        """Error code"""
        cdef int errorcode = MPI_SUCCESS
        errorcode = self.ob_mpi
        return errorcode

    property error_code:
        """error code"""
        def __get__(self):
            return self.Get_error_code()

    def Get_error_class(self):
        """
        Error class
        """
        cdef int errorclass = MPI_SUCCESS
        CHKERR( MPI_Error_class(self.ob_mpi, &errorclass) )
        return errorclass

    property error_class:
        """error class"""
        def __get__(self):
            return self.Get_error_class()

    def Get_error_string(self):
        """
        Error string
        """
        cdef char string[MPI_MAX_ERROR_STRING+1]
        cdef int resultlen = 0
        CHKERR( MPI_Error_string(self.ob_mpi, string, &resultlen) )
        return string

    property error_string:
        """error string"""
        def __get__(self):
            return self.Get_error_string()

def Get_error_class(int errorcode):
    """
    Convert an error code into an error class
    """
    cdef int errorclass = MPI_SUCCESS
    CHKERR( MPI_Error_class(errorcode, &errorclass) )
    return errorclass

def Get_error_string(int errorcode):
    """
    Return a string for a given error code
    """
    cdef char string[MPI_MAX_ERROR_STRING+1]
    cdef int resultlen = 0
    CHKERR( MPI_Error_string(errorcode, string, &resultlen) )
    return string

# Actually no errors
SUCCESS      = MPI_SUCCESS
ERR_LASTCODE = MPI_ERR_LASTCODE

# MPI-1 Error classes
# -------------------
# MPI-1 Objects
ERR_COMM      = MPI_ERR_COMM
ERR_GROUP     = MPI_ERR_GROUP
ERR_TYPE      = MPI_ERR_TYPE
ERR_REQUEST   = MPI_ERR_REQUEST
ERR_OP        = MPI_ERR_OP
# Communication argument parameters
ERR_BUFFER    = MPI_ERR_BUFFER
ERR_COUNT     = MPI_ERR_COUNT
ERR_TAG       = MPI_ERR_TAG
ERR_RANK      = MPI_ERR_RANK
ERR_ROOT      = MPI_ERR_ROOT
ERR_TRUNCATE  = MPI_ERR_TRUNCATE
# Multiple completion
ERR_IN_STATUS = MPI_ERR_IN_STATUS
ERR_PENDING   = MPI_ERR_PENDING
# Topology argument parameters
ERR_TOPOLOGY  = MPI_ERR_TOPOLOGY
ERR_DIMS      = MPI_ERR_DIMS
# Other arguments parameters
ERR_ARG       = MPI_ERR_ARG
# Other errors
ERR_OTHER     = MPI_ERR_OTHER
ERR_UNKNOWN   = MPI_ERR_UNKNOWN
ERR_INTERN    = MPI_ERR_INTERN

# MPI-2 Error classes
# -------------------
# MPI-2 Objects
ERR_INFO                   = MPI_ERR_INFO
ERR_FILE                   = MPI_ERR_FILE
ERR_WIN                    = MPI_ERR_WIN
# Object attributes
ERR_KEYVAL                 = MPI_ERR_KEYVAL
# Info Object
ERR_INFO_KEY               = MPI_ERR_INFO_KEY
ERR_INFO_VALUE             = MPI_ERR_INFO_VALUE
ERR_INFO_NOKEY             = MPI_ERR_INFO_NOKEY
# Input/Ouput
ERR_ACCESS                 = MPI_ERR_ACCESS
ERR_AMODE                  = MPI_ERR_AMODE
ERR_BAD_FILE               = MPI_ERR_BAD_FILE
ERR_FILE_EXISTS            = MPI_ERR_FILE_EXISTS
ERR_FILE_IN_USE            = MPI_ERR_FILE_IN_USE
ERR_NO_SPACE               = MPI_ERR_NO_SPACE
ERR_NO_SUCH_FILE           = MPI_ERR_NO_SUCH_FILE
ERR_IO                     = MPI_ERR_IO
ERR_READ_ONLY              = MPI_ERR_READ_ONLY
ERR_CONVERSION             = MPI_ERR_CONVERSION
ERR_DUP_DATAREP            = MPI_ERR_DUP_DATAREP
ERR_UNSUPPORTED_DATAREP    = MPI_ERR_UNSUPPORTED_DATAREP
ERR_UNSUPPORTED_OPERATION  = MPI_ERR_UNSUPPORTED_OPERATION
# Dynamic Process Management
ERR_NAME                   = MPI_ERR_NAME
ERR_NO_MEM                 = MPI_ERR_NO_MEM
ERR_NOT_SAME               = MPI_ERR_NOT_SAME
ERR_PORT                   = MPI_ERR_PORT
ERR_QUOTA                  = MPI_ERR_QUOTA
ERR_SERVICE                = MPI_ERR_SERVICE
ERR_SPAWN                  = MPI_ERR_SPAWN
# Windows
ERR_BASE                   = MPI_ERR_BASE
ERR_LOCKTYPE               = MPI_ERR_LOCKTYPE
ERR_RMA_CONFLICT           = MPI_ERR_RMA_CONFLICT
ERR_RMA_SYNC               = MPI_ERR_RMA_SYNC
ERR_SIZE                   = MPI_ERR_SIZE
ERR_DISP                   = MPI_ERR_DISP
ERR_ASSERT                 = MPI_ERR_ASSERT
