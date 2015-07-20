function Search()
{
	$("#searchForm").submit();
}

function Init()
{
	$("#searchBtn").click(Search);	
}

$(document).ready(function () 
{
	Init();
});
