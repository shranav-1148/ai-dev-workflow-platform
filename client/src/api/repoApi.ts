export const getRepos = async () => {
  const res = await fetch("/api/repos")

  if (!res.ok) {
    throw new Error("Failed to fetch repos")
  }

  return res.json()
}
