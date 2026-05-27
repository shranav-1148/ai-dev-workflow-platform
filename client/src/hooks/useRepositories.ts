// hooks/useRepositories.ts

import { useQuery } from "@tanstack/react-query"
import { getRepos } from "@/api/repoApi"

export const useRepositories = () => {
  return useQuery({
    queryKey: ["repos"],
    queryFn: getRepos
  })
}