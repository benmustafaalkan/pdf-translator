import git
import os
from typing import Tuple

class GitManager:
    def __init__(self, repo_path=None):
        self.repo_path = repo_path or os.getcwd()
        try:
            self.repo = git.Repo(self.repo_path)
        except git.exc.InvalidGitRepositoryError:
            self.repo = None
    
    def is_git_repo(self) -> bool:
        return self.repo is not None
    
    def get_status(self) -> str:
        if not self.repo:
            return "Bu klasör bir git deposu değil."
        return self.repo.git.status()
    
    def add_all(self) -> Tuple[bool, str]:
        if not self.repo:
            return False, "Git deposu bulunamadı."
        try:
            self.repo.git.add(A=True)
            return True, "Tüm değişiklikler eklendi."
        except Exception as e:
            return False, str(e)
    
    def commit(self, message: str) -> Tuple[bool, str]:
        if not self.repo:
            return False, "Git deposu bulunamadı."
        try:
            self.repo.index.commit(message)
            return True, "Commit başarılı."
        except Exception as e:
            return False, str(e)
    
    def push(self) -> Tuple[bool, str]:
        if not self.repo:
            return False, "Git deposu bulunamadı."
        try:
            origin = self.repo.remote(name='origin')
            origin.push()
            return True, "Push başarılı."
        except Exception as e:
            return False, str(e)
    
    def pull(self) -> Tuple[bool, str]:
        if not self.repo:
            return False, "Git deposu bulunamadı."
        try:
            origin = self.repo.remote(name='origin')
            origin.pull()
            return True, "Pull başarılı."
        except Exception as e:
            return False, str(e) 