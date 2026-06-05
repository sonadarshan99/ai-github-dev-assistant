import os
import subprocess
from git import Repo


class AutoPatchEngine:

    def __init__(self, repo_url):

        self.repo_url = repo_url

        self.local_path = "repo_temp"

        self.repo = None
        self.local_repo = None

        self.clone_repo()


    # ---------------- SAFE CLONE ----------------
    def clone_repo(self):

        try:
            if os.path.exists(self.local_path):
                print("📁 Repo already exists, skipping clone")
                self.local_repo = Repo(self.local_path)
                return

            print("📥 Shallow cloning repo (SAFE MODE)...")

            subprocess.run(
                [
                    "git",
                    "clone",
                    "--depth", "1",
                    "--single-branch",
                    self.repo_url,
                    self.local_path
                ],
                check=True
            )

            print("✅ Clone successful")

            self.local_repo = Repo(self.local_path)

        except Exception as e:
            print("❌ Clone failed:", e)
            raise


    # ---------------- PATCH APPLY ENGINE ----------------
    def run_fix(self, fix, commit_message="ai fix"):

        """
        fix format:
        {
            "file_path": "...",
            "old_code": "...",
            "new_code": "...",
            "reason": "..."
        }
        """

        try:

            file_path = fix.get("file_path")

            old_code = fix.get("old_code", "")
            new_code = fix.get("new_code", "")

            if not file_path:
                print("❌ Missing file path")
                return False

            full_path = os.path.join(self.local_path, file_path)

            if not os.path.exists(full_path):
                print(f"❌ File not found: {file_path}")
                return False

            print(f"✏️ Editing file: {file_path}")

            # read file
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # replace logic (safe fallback)
            if old_code and old_code in content:
                content = content.replace(old_code, new_code)
            else:
                # fallback: append fix
                content += "\n\n# AI FIX APPLIED\n" + new_code

            # write file
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

            # git commit
            repo = Repo(self.local_path)
            repo.git.add(A=True)

            if repo.is_dirty():

                repo.index.commit(commit_message)

                print("✅ Commit created")

                return True

            print("⚠️ No changes detected")

            return False


        except Exception as e:
            print("❌ Patch error:", e)
            return False