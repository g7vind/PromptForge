import argparse
import sys
import traceback

from agent.graph import agent
from agent.tools import list_projects, get_current_project_name


def main():
    parser = argparse.ArgumentParser(description="Run engineering project planner")
    parser.add_argument("--recursion-limit", "-r", type=int, default=100,
                        help="Recursion limit for processing (default: 100)")
    parser.add_argument("--list-projects", "-l", action="store_true",
                        help="List all existing projects")

    args = parser.parse_args()

    try:
        # List projects if requested
        if args.list_projects:
            projects = list_projects()
            if projects:
                print("📂 Existing projects:")
                for i, project in enumerate(projects, 1):
                    print(f"  {i}. {project}")
            else:
                print("No projects found.")
            return

        # Get user prompt
        user_prompt = input("Enter your project prompt: ")
        
        print("\n" + "="*50)
        print("🚀 Starting project generation...")
        print("="*50 + "\n")
        
        # Run the agent
        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": args.recursion_limit}
        )
        
        print("\n" + "="*50)
        print("✅ Project generation completed!")
        if get_current_project_name():
            print(f"📁 Project name: {get_current_project_name()}")
        print("="*50)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print("\n" + "="*50)
        print("❌ Error occurred:")
        print("="*50)
        traceback.print_exc()
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()