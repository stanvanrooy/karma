import {mergeStyleSets} from "@fluentui/react";

export interface ILabelProps {
  label: string;
  value: string;
}

export const Label: React.FC<ILabelProps> = (props) => {
  const { label, value } = props;

  const labelsToIgnore = ['alertname']
  if (labelsToIgnore.includes(label)) {
    return null;
  }

  const styles = mergeStyleSets({
    label: {
      backgroundColor: stringToRgb(label),
      padding: 8,
    }
  });

  return <span className={styles.label}>
    {value}
  </span>
};

const stringToRgb = (s: string): string => {
    // Should look pretty good for most random colors.
    let hash = 0;
    for (var i = 0; i < s.length; i++) {
        hash = s.charCodeAt(i) + ((hash << 5) - hash);
        hash = hash & hash;
    }

    let rgb = [0, 0, 0];
    for (var i = 0; i < 3; i++) {
        var value = (hash >> (i * 8)) & 255;
        rgb[i] = value;
    }

    const hsv = rgbToHsv(rgb);
    hsv[1] *= 0.6;
    hsv[2] *= 1.5;
    rgb = hsvToRgb(hsv);
    return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
}

const rgbToHsv = (color: number[]): number[] => {
  const [r, g, b] = color;
  const min = Math.min( r, g, b );
  const max = Math.max( r, g, b );

  let v = max;
  let delta = max - min;

  let s, h;
  if( max != 0 )
      s = delta / max;
  else {
      s = 0;
      h = -1;
      return [h, s, 0];
  }
  if( r === max )
      h = ( g - b ) / delta;
  else if( g === max )
      h = 2 + ( b - r ) / delta;
  else
      h = 4 + ( r - g ) / delta;
  h *= 60;
  if( h < 0 )
      h += 360;
  if ( isNaN(h) )
      h = 0;
  return [h,s,v];
};

const hsvToRgb = (color: number[]): number[] => {
  let [h, s, v] = color;

  let r, g, b, i, f, p, q, t;
  if(s === 0 ) {
      r = g = b = v;
      return [r,g,b];
  }

  h /= 60;
  i = Math.floor( h );
  f = h - i;          // factorial part of h
  p = v * ( 1 - s );
  q = v * ( 1 - s * f );
  t = v * ( 1 - s * ( 1 - f ) );
  switch( i ) {
      case 0:
          r = v;
          g = t;
          b = p;
          break;
      case 1:
          r = q;
          g = v;
          b = p;
          break;
      case 2:
          r = p;
          g = v;
          b = t;
          break;
      case 3:
          r = p;
          g = q;
          b = v;
          break;
      case 4:
          r = t;
          g = p;
          b = v;
          break;
      default:
          r = v;
          g = p;
          b = q;
          break;
  }
  return [r,g,b];
}

