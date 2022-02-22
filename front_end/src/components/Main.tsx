import { useEthers } from "@usedapp/core"
import helperConfig from "../helper-config.json"

export const Main = () => {

    const { chainId } = useEthers()
    const networkName = chainId ? helperConfig[chainId] : "dev"
    console.log(chainId)
    console.log(networkName)

return (<>
    <h2 >Dapp Token App</h2>
    </>)
}