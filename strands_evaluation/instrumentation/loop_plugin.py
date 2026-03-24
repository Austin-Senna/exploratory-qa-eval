import logging
from strands.vended_plugins.steering import Guide, Proceed, SteeringHandler, ToolSteeringAction

logger = logging.getLogger(__name__)

class CategoryStagnationHandler(SteeringHandler):
    name = "category-stagnation"

    def __init__(self, max_consecutive_category: int = 4):
        super().__init__()
        self.max_consecutive = max_consecutive_category
        self.last_category = None
        self.consecutive_count = 0
        
        # Track total times we had to intervene in this run
        self.total_loop_interventions = 0 

        # Define your tool buckets
        self.tool_categories = {
            "search": {"search", "search_keyword", "search_prefix", "search_value", "search_schema", "search_reranked"},
            "inspect": {"list_files", "peek_file", "peek_files", "get_sandbox_info", "read_file"},
            "execute": {"execute_code", "query_file", "grep_file"}
        }

    def _get_category(self, tool_name: str) -> str:
        for category, tools in self.tool_categories.items():
            if tool_name in tools:
                return category
        return "other"

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        tool_name = tool_use.get("name")
        
        if tool_name in ["submit_answer", "plan", "download"]:
            self.last_category = "terminal_or_plan"
            self.consecutive_count = 0
            return Proceed(reason="Allowed tool")

        current_category = self._get_category(tool_name)

        if current_category == self.last_category:
            self.consecutive_count += 1
        else:
            self.last_category = current_category
            self.consecutive_count = 1

        if self.consecutive_count > self.max_consecutive:
            # Increment the counter and log to the console/file
            self.total_loop_interventions += 1
            logger.warning(
                f"[Stagnation Detector] Intercepted loop! Category '{current_category}' "
                f"called {self.consecutive_count} times. "
                f"(Total interventions this run: {self.total_loop_interventions})"
            )
            
            self.consecutive_count = 0 
            
            return Guide(
                reason=(
                    f"SYSTEM INTERRUPTION: You have used '{current_category}' type tools "
                    f"more than {self.max_consecutive} times in a row likely without making meaningful progress. "
                    "You are likely stuck in a loop.\n\n"
                    "If you believe so, DO NOT repeat this action. You must step back and use the `plan` tool immediately "
                    "to rethink your strategy. The `plan` tool is free and will help you figure out if you "
                    "should skip this dataset, guess based on context, or try a completely different approach."
                )
            )

        return Proceed(reason="No categorical stagnation detected")