#include <stdint.h>

char errMessage[MAX_ERRNO][27] =
{
	"Unknown error code!",
	"Yet unimplemented feature!",
	"Unsupported architecture!",
	"Out of range!",
	"Object already exists!",
	"A subroutine failed!"
};

char * getErrText(const err_t errCode);

bool assertSuccess(const err_t errCode)
{
	if(errCode != SUCCESS)
	{
		//will halt the kernel, no return needed
		fatalErr("%s", getErrText(errCode));
	}
	return true;
}

bool verify(const err_t errCode)
{
	if(errCode != SUCCESS)
	{
		printErr("%s", getErrText(errCode));
		return false;
	}
	return true;
}
