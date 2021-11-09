

export function strFirstUpper(string){
    var lower = string.toString().toLowerCase();
    return lower.charAt(0).toUpperCase() + lower.slice(1)
}
