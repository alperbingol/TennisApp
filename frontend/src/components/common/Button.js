function Button({ onClick, children, className = '', disabled = false, ...props }) {
  return (
    <button 
      className={className}
      onClick={onClick}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}

export default Button;