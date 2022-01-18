import {INavLinkGroup, INavProps, Nav} from "@fluentui/react"
import {useConst} from "@fluentui/react-hooks"
import React from "react"

export interface INavigationProps {
  className?: string;
}

export const Navigation: React.FC<INavigationProps> = (props) => {
  const navProps: INavLinkGroup[] = useConst([{
    name: 'Karma',
    links: [
      { key: 'alert-overview', name: 'Overview', url: '/alerts' }
    ]
  }]);

  return <Nav className={props.className} groups={navProps} />
}

